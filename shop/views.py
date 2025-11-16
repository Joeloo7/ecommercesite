from idlelib.debugobj import dispatch

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views import View
from shop.models import Category,Product
class Categoryview(View):
    def get(self,request):
        c=Category.objects.all()
        context={'categories':c}
        return render(request,'category.html',context)
# Create your views here.
class ProductView(View):
    def get(self,request,i):
        c = Category.objects.get(id=i)
        context = {'category': c}
        return render(request,'product.html',context)
class DetailView(View):
    def get(self,request,i):
        p=Product.objects.get(id=i)
        context={'product':p}
        return render(request,'detail.html',context)
from shop.forms import SignupForm,LoginForm,ProductForm,CategoryForm,StockForm
class RegisterView(View):
    def get(self,request):
        form_instance=SignupForm()
        context={'form':form_instance}
        return render(request,'register.html',context)
    def post(self,request):
        form_instance=SignupForm(request.POST)
        if form_instance.is_valid():
            form_instance.save()
            return redirect('shop:login')
        else:
            print('error')
            return render(request,'register.html',{'form':form_instance})
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
class LoginView(View):
    def post(self,request):
        form_instance=LoginForm(request.POST)
        if form_instance.is_valid():
            u=form_instance.cleaned_data['username']
            p=form_instance.cleaned_data['password']
            user=authenticate(username=u,password=p)
            if user and user.is_superuser == True:
                login(request,user)
                return redirect('shop:category')
            elif user and user.is_superuser != True:
                login(request, user)
                return redirect('shop:category')
            else:
                messages.error(request,'invalid credentials')
                return render(request,'login.html',{'form':form_instance})

    def get(self,request):
        form_instance=LoginForm()
        context={'form':form_instance}
        return render(request,'login.html',context)
class LogoutView(View):
    def get(self,request):
        logout(request)
        return redirect('shop:login')
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
def admin_required(fun):
    def wrapper(request):
        if request.user.is_Superuser:
            return HttpResponse('not allowed')
        else:
            return fun(request)
    return wrapper
@method_decorator(admin_required,name="dispatch")
@method_decorator(login_required,name="dispatch")
class AddCategoryView(View):
    def post(self,request):
        form_instance=CategoryForm(request.POST,request.FILES)
        if form_instance.is_valid():
            form_instance.save()
            return redirect('shop:category')
        else:
            print('error')
            return render(request,'addcategories.html',{'form':form_instance})
    def get(self,request):
        form_instance = CategoryForm()
        context = {'form': form_instance}
        return render(request, 'addcategories.html',context)
class AddProductView(View):
    def post(self,request):
        form_instance=ProductForm(request.POST,request.FILES)
        if form_instance.is_valid():
            form_instance.save()
            return redirect('shop:category')
        else:
            print('error')
            return render(request,'addproducts.html',{'form':form_instance})
    def get(self,request):
        form_instance = ProductForm()
        context = {'form': form_instance}
        return render(request, 'addproducts.html', context)
class AddStockView(View):
    def post(self,request,i):
        p=Product.objects.get(id=1)
        form_instance=StockForm(request.POST,instance=p)
        if form_instance.is_valid():
            form_instance.save()
            return redirect('shop:category')
        else:
            print('error')
            return render(request,'addstock.html',{'form':form_instance})
    def get(self,request):
        p=Product.objects.get(id=1)
        form_instance = StockForm(instance=p)
        context = {'form': form_instance}
        return render(request, 'addstock.html', context)