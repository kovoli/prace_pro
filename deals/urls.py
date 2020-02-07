from django.urls import path
from . import views

app_name = 'deals'

urlpatterns = [
    path('', views.home_page, name='home'),
    path('deal/<slug:slug>/', views.deal_single, name='deal_detail'),
    path('like_comment/', views.like_comment, name='like_comment'),
    path('like_dislike/like/', views.like_deal, name='like_like'),
    path('like_dislike/dislike/', views.dislike_deal, name='like_dislike'),
    path('category/<slug:slug>/', views.deals_by_category, name='deals_by_category'),
    path('shop/<slug:slug>/', views.deals_by_shop, name='deals_by_shop'),
]
