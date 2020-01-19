from django.shortcuts import render, get_object_or_404, redirect
from .models import Deal, Category, Brand, Shop, Comment
from django.http import HttpResponse, JsonResponse
from .forms import CommentForm
import json
from . import helpers
from django.db.models import F
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST


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


#@login_required
@require_POST
def like_comment(request):
    object_id = request.POST.get('id', None)
    if request.is_ajax() and request.POST and object_id:
        request.session.set_expiry(180)
        num_click = request.session.get('click', 0)
        if num_click == 0:
            comment = get_object_or_404(Comment, id=object_id)
            comment.like = F('like') + 1
            comment.save()
            comment.refresh_from_db(fields=['like'])
            request.session['click'] = num_click + 1
            data = {'comment': comment.like, 'id': f"{comment.id}"}
        else:
            comment = get_object_or_404(Comment, id=object_id)
            comment.like = F('like') - 1
            comment.save()
            comment.refresh_from_db(fields=['like'])
            request.session['click'] = num_click - 1
            data = {'comment': comment.like, 'id': f"{comment.id}"}
        return HttpResponse(json.dumps(data), content_type='application/json')
    else:
        return JsonResponse({'error': 'Only aasdfa'}, status=404)



# def like(request, pk):
#     obj = Article.objects.get(pk=pk)
#     try:
#         likedislike = LikeDislike.objects.get(content_type=ContentType.objects.get_for_model(obj), object_id=obj.id,
#                                               user=request.user)
#         if likedislike.vote is not LikeDislike.LIKE:
#             likedislike.vote = LikeDislike.LIKE
#             likedislike.save(update_fields=['vote'])
#             result = True
#         else:
#             likedislike.delete()
#             result = False
#     except LikeDislike.DoesNotExist:
#         obj.votes.create(user=request.user, vote=LikeDislike.LIKE)
#         result = True
#
#     return HttpResponse(
#         json.dumps({
#             "result": result,
#             "like_count": obj.votes.likes().count(),
#             "dislike_count": obj.votes.dislikes().count(),
#             "sum_rating": obj.votes.sum_rating()
#         }),
#         content_type="application/json"
#     )