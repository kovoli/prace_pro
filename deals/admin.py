from django.contrib import admin
from .models import Category, Deal, Brand, Shop, Comment


@admin.register(Deal)
class DealAdmin(admin.ModelAdmin):
    list_display = ['name']
    list_filter = ['category']
    readonly_fields = ['slug']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
    readonly_fields = ['slug']


@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    list_display = ['name']
    readonly_fields = ['slug']


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ['name']
    readonly_fields = ['slug']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['author', 'deal', 'body']
