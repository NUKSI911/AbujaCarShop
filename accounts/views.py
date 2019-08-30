    # -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.http import is_safe_url
from django.shortcuts import render,redirect
from .models import GuestEmail
from .forms import LoginForm,RegisterForm,GuestForm
from django.contrib.auth import get_user_model,login,authenticate
from django.views.generic import CreateView,FormView
from .signals import user_logged_in
# Create your views here.


User=get_user_model()
def guest_register_view(request):
    form=GuestForm(request.POST or None)
    context={"form":form } 
    next_ = request.GET.get('next')
    next_post=request.POST.get('next')
    redirect_path=next_ or next_post or None
    if form.is_valid():
        # print(form.cleaned_data)
        email=form.cleaned_data.get('email')
        new_guest_email=GuestEmail.objects.create(email=email)
        request.session['guest_email_id']=new_guest_email.id
        if is_safe_url(redirect_path,request.get_host()):
            return redirect (redirect_path)   
        else:
            return redirect('carts:checkout') 
            
    else:
            print("Error")
    return redirect("carts:checkout")


class LoginView(FormView):
    form_class=LoginForm
    success_url="/"
    template_name='accounts/login.html'
    def form_valid(self,form):
        request=self.request
        print(request.user.is_authenticated())
        next_ = request.GET.get('next')
        ext_post=request.POST.get('next')
        redirect_path=next_ or next_post or None
        email=form.cleaned_data.get('email')
        password=form.cleaned_data.get('password')
        user=authenticate(request,username=email,password=password)
        if user is not None:
            login(request,user)
            user_loggged_in.send(user.__class__,isinstance=user,request=request)
            try:
                del request.session['guest_email_id']
            except:
                pass
            if is_safe_url(redirect_path,request.get_host()):
                return redirect(redirect_path)   
            else:
                return redirect('/') 
        return super(LoginView,self).form_invalid()

# def login_page(request):
#     form=LoginForm(request.POST or None)
#     context={"form":form } 
#     print("User logged in")
#     print(request.user.is_authenticated())
#     next_ = request.GET.get('next')
#     next_post=request.POST.get('next')
#     redirect_path=next_ or next_post or None
#     if form.is_valid():
#         print(form.cleaned_data)
#         username=form.cleaned_data.get('username')
#         password=form.cleaned_data.get('password')
#         user=authenticate(request,username=username,password=password)
#         if user is not None:
#             login(request,user)
#             try:
#                 del request.session['guest_email_id']
#             except:
#                 pass
#             if is_safe_url(redirect_path,request.get_host()):
#                 return redirect(redirect_path)   
#             else:
#                 return redirect('/') 
            
#         else:
#             print("Error")
#     return render(request,"accounts/login.html" ,context )

class RegisterView(CreateView):
    form_class=RegisterForm
    template_name='/accounts/register.html'
    success_url='/login/'





# def register_page(request):
#     form=RegisterForm(request.POST or None)
#     context={
#         "form":form
#     }
#     if form.is_valid():
#         form.save()
#         # print(form.cleaned_data)
#         # username=form.cleaned_data.get('username')
#         # email=form.cleaned_data.get('email')
#         # password=form.cleaned_data.get('password')

#         # new_user=User.objects.create_user(username,password,email)
#         # print(new_user)
#     return render(request,"accounts/register.html" ,context )