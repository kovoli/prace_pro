from django.shortcuts import render, get_object_or_404
from .models import Deal, Category, Brand, Shop


def home_page(request):
    deals = Deal.objects.all()

    context = {'deals': deals}
    return render(request, 'home_page.html', context)


def deal_single(request, slug):
    deal = get_object_or_404(Deal, slug=slug)
    category = Category.objects.root_nodes()
    context = {'deal': deal, 'category': category}

    return render(request, 'deals/deal_single.html', context)
