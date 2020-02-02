from django.shortcuts import render, get_object_or_404, redirect
from .models import Deal, Category, Brand, Shop, Comment
from django.http import HttpResponse, JsonResponse
from .forms import CommentForm
import json
from . import helpers
from django.db.models import F
# decorators
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from common.decorators import ajax_required
# sessions
from .click import ClickComment, ClickDeal


def home_page(request):
    deals = Deal.objects.all().prefetch_related('comments', 'user_like')
    categories = Category.objects.root_nodes()
    deals_list = helpers.pg_records(request, deals, 20)

    context = {'deals_list': deals_list, 'categories': categories}
    return render(request, 'home_page.html', context)


def deal_single(request, slug):
    # Скидка
    deal = get_object_or_404(Deal, slug=slug)
    # Категории
    categories = Category.objects.root_nodes()
    # Комментраии
    comments = deal.comments.filter(active=True)
    semilar_products = Deal.objects.filter(category=deal.category) \
        .exclude(id=deal.id)
    # Форма для комментариев
    new_comment = None

    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST or None)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.deal = deal
            new_comment.save()
            return redirect('deals:deal_detail', slug=deal.slug)
    else:
        comment_form = CommentForm()

    context = {'deal': deal,
               'categories': categories,
               'comments': comments,
               'new_comment': new_comment,
               'comment_form': comment_form,
               'semilar_products': semilar_products}

    return render(request, 'deals/deal_single.html', context)


def deals_by_category(request, slug):
    category = get_object_or_404(Category, slug=slug)
    categories = category.get_descendants().order_by('tree_id', 'id', 'name')
    deals = Deal.objects.filter(category__in=category.get_descendants(include_self=True)).prefetch_related('comments', 'user_like')
    print(request.META.get('HTTP_REFERER', '/'))
    deals_list = helpers.pg_records(request, deals, 20)

    content = {'category': category, 'deals_list': deals_list, 'categories': categories}
    return render(request, 'deals/deal_cat_list.html', content)


# TODO set crontab to delete expired sessions
# @login_required
@require_POST
@ajax_required
def like_comment(request):
    object_id = request.POST.get('id', None)
    click = ClickComment(request)
    if object_id:
        comment = get_object_or_404(Comment, id=object_id)
        click.action_click(comment_id=comment.id)
        comment.like = F('like') + int(request.session['click'][str(object_id)])
        comment.save()
        comment.refresh_from_db(fields=['like'])
        data = {'comment': comment.like, 'id': comment.id}
        return HttpResponse(json.dumps(data), content_type='application/json')
    else:
        return JsonResponse({'error': 'Only aasdfa'}, status=404)


# @login_required
@require_POST
@ajax_required
def like_deal(request):
    deal_id = request.POST.get('id', None)
    like_deal = ClickDeal(request)
    if deal_id:
        if not request.user.is_anonymous:  # Если пользователь в системе
            deal = get_object_or_404(Deal, id=deal_id)
            like_deal.action_click(deal_id=deal.id)
            deal.like_counter = F('like_counter') + 1
            deal.user_like.add(request.user)
            deal.save()
            deal.refresh_from_db(fields=['like_counter'])
            ses = request.session['click_deal']
            data = {'deal_counter': deal.like_counter, 'id': deal.id, 'session_data': ses}
            return JsonResponse(data)
        else:
            deal = get_object_or_404(Deal, id=deal_id)
            like_deal.action_click(deal_id=deal.id)
            deal.like_counter = F('like_counter') + 1
            deal.save()
            deal.refresh_from_db(fields=['like_counter'])
            ses = request.session['click_deal']
            data = {'deal_counter': deal.like_counter, 'id': deal.id, 'session_data': ses}
            print(data['session_data'][str(deal.id)])
            return HttpResponse(json.dumps(data), content_type='application/json')
    else:
        return JsonResponse({'error': 'error'}, status=404)

@require_POST
@ajax_required
def dislike_deal(request):
    deal_id = request.POST.get('id', None)
    like_deal = ClickDeal(request)
    if deal_id:
        if not request.user.is_anonymous:  # Если пользователь в системе
            deal = get_object_or_404(Deal, id=deal_id)
            like_deal.action_click(deal_id=deal.id)
            deal.like_counter = F('like_counter') - 1
            deal.user_like.add(request.user)
            deal.save()
            deal.refresh_from_db(fields=['like_counter'])
            ses = request.session['click_deal']
            data = {'deal_counter': deal.like_counter, 'id': deal.id, 'session_data': ses}
            return JsonResponse(data)
        else:
            deal = get_object_or_404(Deal, id=deal_id)
            like_deal.action_click(deal_id=deal.id)
            deal.like_counter = F('like_counter') - 1
            deal.save()
            deal.refresh_from_db(fields=['like_counter'])
            ses = request.session['click_deal']
            data = {'deal_counter': deal.like_counter, 'id': deal.id, 'session_data': ses}
            return HttpResponse(json.dumps(data), content_type='application/json')
    else:
        return JsonResponse({'error': 'error'}, status=404)

