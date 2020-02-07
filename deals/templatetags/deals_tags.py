from django import template
from deals.models import Deal, Shop

register = template.Library()


@register.inclusion_tag('deals/sidebar/best_deals.html')
def show_best_deals(count=10):
    best_all_time = Deal.objects.all().order_by('-like_counter')[:count]
    return {'best_all_time': best_all_time}


@register.inclusion_tag('deals/sidebar/best_shops.html')
def show_favorite_shops(count=10):
    favorite_shops = Shop.objects.filter(favorites=True)[:count]
    return {'favorite_shops': favorite_shops}


