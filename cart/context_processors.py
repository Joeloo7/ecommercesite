from django.db.models.fields import return_None
from cart.models import Cart

def count(request):
    try:
        u=request.user
        c=Cart.objects.filter(user=u)
        total=0

        for i in c:
            total+=i.quantity
    except:
        total=0
    return {'count':total}