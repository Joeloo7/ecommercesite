from django.contrib import admin
from django.urls import path
from cart import views




app_name='cart'
urlpatterns = [
    path('addtocart/<int:i>',views.AddtoCart.as_view(),name='addtocart'),
    path('cartview',views.CartView.as_view(),name='cartview'),
    path('cartdecrement/<int:i>',views.Cartdecrement.as_view(),name='cartdecrement'),
    path('cartremove/<int:i>',views.Cartremove.as_view(),name='cartremove'),
    path('checkout',views.Checkout.as_view(),name='checkout'),
    path('payment/<i>',views.Payment_success.as_view(),name='success'),
    path('orders', views.Orders.as_view(), name='orders'),
]