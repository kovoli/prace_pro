from django.core.management.base import BaseCommand
from deals.models import Deal, Brand, Category, Shop


from django.core.files.base import ContentFile
from io import BytesIO
from urllib.request import urlopen
from .helpers import open_csv

# ----- Main Command -----
class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        data = open_csv()

        data = {
                'author': 'user',

                }
