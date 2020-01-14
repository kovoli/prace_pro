from django.urls import path
from . import views


urlpatterns = [
    path('', views.home_page, name='home'),
    path('deal/<slug:slug>/', views.deal_single, name='deal_single')
]