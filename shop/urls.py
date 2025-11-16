from django.contrib import admin
from django.urls import path
from shop import views

from shop.views import ProductView,DetailView



app_name='shop'
urlpatterns = [
    path('',views.Categoryview.as_view(),name='category'),
    path('product/<int:i>',views.ProductView.as_view(),name='product'),
    path('details/<int:i>',views.DetailView.as_view(),name='details'),
    path('register', views.RegisterView.as_view(), name='register'),
    path('login', views.LoginView.as_view(), name='login'),
    path('logout', views.LogoutView.as_view(), name='logout'),
    path('addproducts', views.AddProductView.as_view(), name='addproducts'),
    path('addcategories', views.AddCategoryView.as_view(), name='addcategories'),
    path('addstock/<int:i>', views.AddStockView.as_view(), name='addstock'),

]