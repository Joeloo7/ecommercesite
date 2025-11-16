from itertools import product

from django.shortcuts import render
from django.views import View
from django.db.models import Q
from shop.models import Product
# Create your views here.
class SearchView(View):
    def get(self,request):
        query=request.GET['q']
        print(query)
        if query:
            p=Product.objects.filter(Q(name__icontains=query)|Q(description__icontains=query)|Q(price__icontains=query))
            context={'products':p}
        return render(request,'search.html',context)