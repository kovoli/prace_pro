from django.shortcuts import render, get_object_or_404
from .models import Deal, Category, Brand, Shop


def home_page(request):
    deals = Deal.objects.all()
    categories = Category.objects.root_nodes()

    context = {'deals': deals, 'categories': categories}
    return render(request, 'home_page.html', context)


def deal_single(request, slug):
    deal = get_object_or_404(Deal, slug=slug)
    categories = Category.objects.root_nodes()
    comments = deal.comments.filter(active=True)

    context = {'deal': deal,
               'categories': categories,
               'comments': comments}

    return render(request, 'deals/deal_single.html', context)
