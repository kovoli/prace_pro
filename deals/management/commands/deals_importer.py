from django.core.management.base import BaseCommand
from deals.models import Deal, Brand, Category, Shop


from django.core.files.base import ContentFile
from io import BytesIO
from urllib.request import urlopen


# ----- Main Command -----
class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        data = {'name': 'deal_name',
                'description': 'description',
                'author': 'user',
                'price': 4654,
                'oldprice': 255,
                'link_to_shop': 'url()',
                'category': 'category',
                'brand': 'brand',
                'shop': 'shop'
                }
