from django.shortcuts import render, get_object_or_404, redirect
from .models import Deal, Category, Brand, Shop
from .forms import CommentForm


def home_page(request):
    deals = Deal.objects.all()
    categories = Category.objects.root_nodes()

    context = {'deals': deals, 'categories': categories}
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
        comment_form = CommentForm(data=request.POST)
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


