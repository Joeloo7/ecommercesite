from django.contrib import admin
from django.urls import path
from shop import views

from shop.views import ProductView
app_name='shop'
urlpatterns = [
    path('',views.Categoryview.as_view(),name='category'),
    path('product/<int:i>',ProductView.as_view(),name='product'),
]