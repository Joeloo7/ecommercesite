from django.db import models
class Category(models.Model):
    name=models.CharField(max_length=20)
    image=models.ImageField(upload_to='categories')
    description=models.TextField()
    def __str__(self):
        return self.name
# Create your models here.
class Product(models.Model):
    name=models.CharField(max_length=20)
    image=models.ImageField(upload_to='product')
    description=models.TextField()
    price=models.IntegerField()
    stock=models.IntegerField()
    available=models.BooleanField(default=True)
    created=models.DateTimeField(auto_now=True)
    updated=models.DateTimeField(auto_now=True)
    category=models.ForeignKey(Category,on_delete=models.CASCADE,related_name='products')
    def __str__(self):
        return self.name