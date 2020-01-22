from django.shortcuts import render, get_object_or_404, redirect
from .models import Deal, Category, Brand, Shop, Comment
from django.http import HttpResponse, JsonResponse
from .forms import CommentForm
import json
from . import helpers
from django.db.models import F
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .click import ClickComment


def home_page(request):
    deals = Deal.objects.all()
    categories = Category.objects.root_nodes()
    deals_list = helpers.pg_records(request, deals, 2)

    context = {'deals_list': deals_list, 'categories': categories}
    return render(request, 'home_page.html', context)


def deal_single(request, slug):
    # Скидка
    deal = get_object_or_404(Deal, slug=slug)
    # Категории
    categories = Category.objects.root_nodes()
    # Комментраии
    comments = deal.comments.filter(active=True)
    # Форма для комментариев
    new_comment = None

    print(request.session.values())
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
               'comment_form': comment_form}

    return render(request, 'deals/deal_single.html', context)

# TODO set crontab to delete expired sessions
@require_POST
def like_comment(request):
    object_id = request.POST.get('id', None)
    click = ClickComment(request)
    if request.is_ajax() and request.POST and object_id:
        comment = get_object_or_404(Comment, id=object_id)
        click.action_click(comment_id=comment.id)
        comment.like = F('like') + int(request.session['click'][str(object_id)])
        comment.save()
        comment.refresh_from_db(fields=['like'])
        data = {'comment': comment.like, 'id': f"{comment.id}"}
        return HttpResponse(json.dumps(data), content_type='application/json')
    else:
        return JsonResponse({'error': 'Only aasdfa'}, status=404)


