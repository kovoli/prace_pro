import os, django, random

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "prace_pro.settings")
django.setup()

from faker import Faker
from deals.models import Category, Shop, Brand, Deal
from django.contrib.auth.models import User

fake = Faker()


def category_dummy(n):
    cat_n = 0
    cat_name = 'Категория'
    for _ in range(n):
        cat_n += 1
        data = {'name': cat_name + f' {cat_n}', 'short_description': fake.first_name() * 10,
                'description': fake.first_name() * 10}
        category = Category(**data)
        category.save()
        for _ in range(3):
            cat_n += 1
            data = {'name': cat_name + f'{cat_n + 1}', 'short_description': fake.first_name() * 10,
                    'description': fake.first_name() * 10, 'parent': category}
            Category.objects.create(**data)

def shop_dummy(n):
    n_n = 0
    shop_name = 'Магазин'
    for _ in range(n):
        n_n += 1
        data = {'name': shop_name + f' {n_n}', 'description': fake.name() * 20,
                'link_to_shop': fake.url()}
        Shop.objects.create(**data)

def brand_dummy(n):
    n_n = 0
    brand_name = 'Бренд'
    for _ in range(n):
        n_n += 1
        data = {'name': brand_name + f' {n_n}', 'description': fake.name() * 20}
        Brand.objects.create(**data)

def deals_dummy(n):
    n_n = 0
    deal_name = 'Скидка'
    user = User.objects.get(username='kovoli')
    category = Category.objects.all()
    brand = Brand.objects.all()
    shop = Shop.objects.all()
    for _ in range(n):
        n_n += 1
        data = {'name': deal_name + f' {n_n}', 'description': fake.name() * 100,
                'author': user, 'price': random.randint(200, 10000), 'oldprice': random.randint(200, 10000),
                'link_to_shop': fake.url(),
                'category': random.choice(category),
                'brand': random.choice(brand),
                'shop': random.choice(shop)}
        Deal.objects.create(**data)
        


#category_dummy(5)
#hop_dummy(5)
#brand_dummy(5)
deals_dummy(100)