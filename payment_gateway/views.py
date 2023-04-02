from django.shortcuts import render
from requests import Request
from .models import *
from django.conf import settings
from instamojo_wrapper import Instamojo
# Create your views here.
from django.http import HttpResponse
api=Instamojo(api_key=settings.API_KEY,
    auth_token=settings.AUTH_TOKEN, endpoint='https://test.instamojo.com/api/1.1/'

)

def home(request):
    products=Product.objects.all()
    return render(request,"home.html",{'products':products})

def order(request,product_id):
    try:
        product_obj=Product.objects.get(uid=product_id)
        order_obj , _=Order.objects.get_or_create(
            product=product_obj,
            user=request.user,
            is_paid=False
        )
        response=api.payment_request_create(
            amount=order_obj.product.prduct_price,
            purpose='Order Process',
            buyer_name="Payal Gupta",
            email="guptapayal9811@gmail.com",
            redirect_url="http://127.0.0.1:8000/order-success/"
        )
        print(response)
        order_obj.order_id=response['payment_request']['id']
        order_obj.instamojo_response=response
        order_obj.save()
        return render(request,"order.html",context={
            'payment_url':response['payment_request']['longurl']
        })
    except Exception as e:
        print(e)

def order_success(request):
    payment_request_id=request.GET.get('payment_request_id')
    order_obj=Order.objects.get(order_id=payment_request_id)
    order_obj.is_paid=True
    order_obj.save()
    return HttpResponse("payment successful")