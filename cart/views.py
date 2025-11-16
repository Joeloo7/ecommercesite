from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from shop.models import Product
from cart.models import Cart
from django.contrib import messages
import razorpay

from cart.models import Order,Order_items


class AddtoCart(View):
    def get(self,request,i):
        p=Product.objects.get(id=i)
        u=request.user
        try:
            c=Cart.objects.get(user=u,product=p)
            c.quantity+=1
            c.save()
        except:
            c=Cart.objects.create(user=u,product=p,quantity=1)
            c.save()
        return redirect('cart:cartview')
class CartView(View):
    def get(self,request):
        u=request.user
        c=Cart.objects.filter(user=u)
        total = 0
        for i in c:
            total += i.product.price * i.quantity
        context = {'cart': c, 'total': total}
        return render(request,'cart.html',context)
class Cartdecrement(View):
    def get(self,request,i):
        p=Product.objects.get(id=i)
        u=request.user
        try:
            c=Cart.objects.get(product=p,user=u)
            if(c.quantity>1):
                c.quantity-=1
                c.save()
            else:
                c.delete()
        except:
            pass
        return redirect('cart:cartview')
class Cartremove(View):
    def get(self,request,i):
        p=Product.objects.get(id=i)
        u=request.user
        try:
            c=Cart.objects.get(product=p,user=u)
            c.delete()
        except:
            pass
        return redirect('cart:cartview')
from cart.forms import OrderForm
def checkstock(c):
    stock=True
    for i in c:
        if i.product.stock<i.quantity:
            stock=False
            break
    else:
        stock=True
    return stock
import uuid
class Checkout(View):
    def post(self,request):
        print(request.POST)
        form_instance=OrderForm(request.POST)
        if form_instance.is_valid():
            o=form_instance.save(commit=False)
            u=request.user
            o.user=u
            c = Cart.objects.filter(user=u)

            total = 0
            for i in c:
                total += i.product.price * i.quantity
            o.amount = total
            o.save()
            if(o.payment_method=='online'):
                client=razorpay.Client(auth=('rzp_test_ReWDUyUM9SBdUY','t6uSZ6L3a3JnA2Cj2UZpZn2e'))
                print(client)
                response_payment=client.order.create(dict(amount=total*100,currency='INR'))
                print(response_payment)
                id=response_payment['id']
                o.order_id=id
                o.save()
                context={'payment':response_payment}
            else:
                o.is_ordered=True
                uid=uuid.uuid4().hex[::14]
                c = Cart.objects.filter(user=u)
                id='order_COD'+uid
                o.order_id=id
                o.save()
                for i in c:
                    items = Order_items.objects.create(order=o, product=i.product, quantity=i.quantity)
                    items.save()
                    items.product.stock -= items.quantity
                    items.product.save()

        return render(request,'payment.html',context)
    def get(self,request):
        u=request.user
        c=Cart.objects.filter(user=u)
        stock=checkstock(c)
        if stock:
            form_instance=OrderForm()
            context={'forms':form_instance}
            return render(request,'checkout.html',context)
        else:
            messages.error(request,'cant place order')
            return render(request, 'checkout.html')
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth import login
@method_decorator(csrf_exempt,name="dispatch")
class Payment_success(View):
    def post(self,request,i):
        u = User.objects.get(username=i)
        login(request, u)
        response=request.POST
        print(response)
        id=response['razorpay_order_id']
        print(id)

        order = Order.objects.get(order_id=id)
        order.is_ordered = True  # after successful completion of order
        order.save()

        # order_items
        c = Cart.objects.filter(user=u)
        for i in c:
            o = Order_items.objects.create(order=order, product=i.product, quantity=i.quantity)
            o.save()
            o.product.stock-=o.quantity
            o.product.save()

            c.delete()
        return render(request,'payment_success.html')
class Orders(View):
    def get(self,request):
        u=request.user
        o=Order.objects.filter(user=u,is_ordered=True)
        context={'orders':o}
        return render(request,'orders.html',context)
# Create your views here.
