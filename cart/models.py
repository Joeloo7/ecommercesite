

from django.db import models

from shop.models import Product
from django.contrib.auth.models import User

class Cart(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity=models.IntegerField()
    date_added=models.DateTimeField(auto_now_add=True)
# Create your models here.
    def __str__(self):
        return self.user.username
    def subtotal(self):
        return self.product.price*self.quantity

from django.utils import timezone
class Order(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    amount=models.IntegerField()
    order_id=models.CharField(max_length=20)
    phone=models.IntegerField(null=True)
    address=models.TextField()
    payment_method=models.CharField(max_length=20)
    order_date=models.DateTimeField(auto_now=True)
    is_ordered = models.BooleanField(default=False)
    delivery_status=models.BooleanField(default=False)
    def __str__(self):
        return self.user.username

class Order_items(models.Model):
    order=models.ForeignKey(Order,on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity=models.IntegerField()
    def __str__(self):
        return self.product.name