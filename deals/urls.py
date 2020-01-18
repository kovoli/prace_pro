from django.urls import path
from . import views

app_name = 'deals'

urlpatterns = [
    path('', views.home_page, name='home'),
    path('deal/<slug:slug>/', views.deal_single, name='deal_detail'),
    path('like_comment/', views.like_comment, name='like_comment')
]
