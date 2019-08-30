# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from products.models import Product 
from accounts.models import GuestEmail
from billing.models import  BillingProfile
from django.http import JsonResponse
from orders.models import Order
from addresses.models import Address
from accounts.forms import LoginForm,GuestForm
from addresses.forms import AddressForm
from django.shortcuts import render,redirect
from .models import Cart
# Create your views here.



def cart_detail_api_view(request):
    cart_obj, new_obj = Cart.objects.new_or_get(request)
    products = [{
            "id": x.id,
            "url": x.get_absolute_url(),
            "name": x.name, 
            "price": x.price
            } 
            for x in cart_obj.products.all()]
    cart_data  = {"products": products, "subtotal": cart_obj.subtotal, "total": cart_obj.total}
    return JsonResponse(cart_data)

def cart_home(request):
    cart_obj,new_obj=Cart.objects.new_or_get(request)
    return render(request,'carts/home.html',{"cart":cart_obj})


def cart_update(request):
    product_id=request.POST.get('product_id')
    if product_id is not None:
        try:
            product_obj = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            print("Show Message To User,product is gone")
            return redirect("carts:home")
        cart_obj,new_obj=Cart.objects.new_or_get(request)
        if product_obj in cart_obj.products.all():
            cart_obj.products.remove(product_obj)
            added=False
        else:
            cart_obj.products.add(product_obj)
            added=True
        request.session['cart_items']=cart_obj.products.count()
        if request.is_ajax(): # Asynchronous JavaScript And XML / JSON
            print("Ajax request")
            json_data = {
            "added": added,
            "removed": not added,
            "cartItemCount": cart_obj.products.count()
            }
            return JsonResponse(json_data, status=200) # HttpResponse
                # return JsonResponse({"message": "Error 400"}, status=400) # Django Rest Framework
    return redirect ("carts:home")

def checkout_home(request):
    cart_obj,cart_created=Cart.objects.new_or_get(request)
    order_obj=None
    if cart_created or cart_obj.products.count()==0:
        return redirect("carts:home")
    login_form=LoginForm()
    guest_form=GuestForm()
    address_form = AddressForm()
    billing_address_id=request.session.get("billing_address_id",None)
    shipping_address_id=request.session.get("shipping_address_id",None)
    billing_profile,billing_profile_created=BillingProfile.objects.new_or_get(request)
    address_qs=None 
    if billing_profile is not None:
            address_qs=Address.objects.filter(billing_profile=billing_profile)
            order_obj,order_obj_created=Order.objects.new_or_get(billing_profile,cart_obj)
            if shipping_address_id:
                order_obj.shipping_address=Address.objects.get(id=shipping_address_id)
                del request.session["shipping_address_id"]
            if billing_address_id:
                order_obj.billing_address=Address.objects.get(id=billing_address_id)
                del request.session["billing_address_id"]
            if billing_address_id or shipping_address_id:
                order_obj.save()
    if request.method=='POST':
        is_done=order_obj.check_done()
        if is_done:
            order_obj.mark_paid()
            request.session['cart_item']=0
            del request.session['cart_id']
            return redirect("carts:success")


      
    context={
        "objects":order_obj,
        "billing_profile":billing_profile,
        "login_form":login_form,
        'guest_form':guest_form,
        "address_form":address_form,
        "address_qs":address_qs
    }
    return render(request,"carts/checkout.html",context)

def checkout_done_view(request):
    return render(request,"carts/checkout_done.html",{})







      # order_qs=Order.objects.filter(billing_profile=billing_profile, cart=cart_obj,active=True)
        # if order_qs.count()==1:

        #     order_obj=order_qs.first()
        # else:
        #     old_order_qs=Order.objects.exclude(billing_profile=billing_profile).filter(cart=cart_obj,active=True)
        #     if old_order_qs.exists():
        #         old_order_qs.update(active=False)
        #     order_obj=Order.objects.create(billing_profile=billing_profile,
        #     cart=cart_obj
        #     )









          # guest_email_id=request.session.get('guest_email_id')
    # if user.is_authenticated():
    #     billing_profile,billing_profile_created=BillingProfile.objects.get_or_create(user=user,email=user.email)
    # elif guest_email_id is not None:
    #     guest_email_obj=GuestEmail.objects.get(id=guest_email_id)
    #     billing_profile,billing_guest_profile_created=BillingProfile.objects.get_or_create(email=guest_email_obj.email)
    # else: 
    #     pass