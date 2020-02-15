from django.shortcuts import render, get_object_or_404, HttpResponseRedirect, reverse
from .models import Deal, Category, Shop, Comment, Brand
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
from .forms import CommentForm, FilterByBrand
import json
from common import helpers
from django.db.models import F
# decorators
# from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from common.decorators import ajax_required
# sessions
from .click import ClickComment, ClickDeal
from django.db.models import Count
# Search
from watson import search as watson


def home_page(request):
    deals = Deal.objects.all().prefetch_related('comments',
                                                'user_like',
                                                'author__profile',
                                                'shop')
    deals_list = helpers.pg_records(request, deals, 20)
    # Категории
    categories = Category.objects.root_nodes()


    context = {'deals_list': deals_list,
               'categories': categories}
    return render(request, 'home_page.html', context)


def deal_single(request, slug):
    # Скидка
    deal = get_object_or_404(Deal.objects.select_related('author__profile', 'category'), slug=slug)
    breadcrumbs = Category.get_ancestors(deal.category, include_self=True)
    # Комментраии
    comments = Comment.objects.filter(deal=deal, active=True).prefetch_related('author')
    # Похожие товары
    semilar_products = Deal.objects.filter(category=deal.category) \
        .annotate(like_count=Count('user_like')).order_by('-like_count').exclude(id=deal.id)[:10]
    # Категории
    categories = Category.objects.root_nodes()

    # Форма для комментариев
    new_comment = None

    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            if request.user.is_authenticated:
                new_comment = comment_form.save(commit=False)
                new_comment.deal = deal
                new_comment.author = User.objects.get(username=request.user)
                new_comment.save()
            else:
                new_comment = comment_form.save(commit=False)
                new_comment.deal = deal
                new_comment.save()
            return HttpResponseRedirect(reverse('deals:deal_detail', args=[deal.slug]))
    else:
        comment_form = CommentForm()

    context = {'deal': deal,
               'breadcrumbs': breadcrumbs,
               'comments': comments,
               'categories': categories,
               'new_comment': new_comment,
               'comment_form': comment_form,
               'semilar_products': semilar_products}

    return render(request, 'deals/deal_single.html', context)


def deals_by_category(request, slug):
    category = get_object_or_404(Category, slug=slug)
    categories = category.get_descendants().order_by('tree_id', 'id', 'name')
    breadcrumbs = Category.get_ancestors(category, include_self=True)
    deals = Deal.objects.filter(category__in=category.get_descendants(include_self=True))\
        .prefetch_related('comments', 'user_like', 'author__profile', 'shop')

    # Brand Filter
    brands_ids = deals.values_list('brand__id', flat=True).order_by().distinct()

    brand_filter = FilterByBrand(request.GET)
    brand_filter.fields['brand'].queryset = Brand.objects.filter(id__in=brands_ids)

    deals_list = helpers.pg_records(request, deals, 20)

    if brand_filter.is_valid() and brand_filter.cleaned_data['brand']:
        deals_list = helpers.pg_records(request, deals.filter(brand__in=brand_filter.cleaned_data['brand']), 20)

    context = {'category': category,
               'deals_list': deals_list,
               'categories': categories,
               'breadcrumbs': breadcrumbs,
               'brand_filter': brand_filter}
    return render(request, 'deals/deal_cat_list.html', context)


def all_categories(request):
    all_categories = Category.objects.root_nodes()
    context = {'all_categories': all_categories}
    return render(request, 'deals/all_categories.html', context)


def deals_by_shop(request, slug):
    shop = get_object_or_404(Shop, slug=slug)
    deals_shop = Deal.objects.filter(shop=shop.id) \
        .prefetch_related('comments', 'user_like', 'author__profile', 'shop')

    deals_list = helpers.pg_records(request, deals_shop, 20)
    # Категории
    categories = Category.objects.root_nodes()

    context = {'shop': shop,
               'deals_list': deals_list,
               'deals_shop': deals_shop,
               'categories': categories}
    return render(request, 'deals/deals_by_shop.html', context)


def search_deals(request):
    if 'q' in request.GET:
        q = request.GET['q']
        search_list = watson.filter(Deal.objects.prefetch_related('comments', 
                                                                  'user_like',
                                                                  'author__profile',
                                                                  'shop'), q)
        deals_list = helpers.pg_records(request, search_list, 54)
    return render(request, 'deals/search_deals.html', {'q': q, 'deals_list': deals_list})


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
#@login_required
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
#@login_required
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

