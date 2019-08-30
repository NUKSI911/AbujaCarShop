"""ecommerce URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from products.views import ProductListView,product_list_view,ProductDetailView,product_detail_view
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin

from django.conf.urls import url,include
from django.contrib.auth.views import LogoutView

from accounts.views import LoginView,RegisterView,guest_register_view
from .views import home_page ,about_page,contact_page,service_page
from carts.views import cart_home,cart_detail_api_view
from addresses.views import checkout_address_create_view,checkout_address_reuse_view
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$',home_page,name='home'),
    url(r'^about/$',about_page,name='about'),
    url(r'^products/',include('products.urls', namespace="products")),
    url(r'^cart/',include('carts.urls', namespace="carts")),
    url(r'^search/',include('search.urls', namespace="search")),
    url(r'^checkout/address/create/$',checkout_address_create_view,name='checkout_address_create'),
    url(r'^contact/$',contact_page,name='contact'),
    url(r'^checkout/address/reuse/$',checkout_address_reuse_view,name='checkout_address_reuse'),    
    url(r'^service/$',service_page,name='service'),
    url(r'^login/$',LoginView.as_view(),name='login'),
    url(r'^register/guest/$',guest_register_view,name='guest_register'),
    url(r'^api/cart/$',cart_detail_api_view,name='api-cart'),
    url(r'^register/$',RegisterView.as_view(),name='register'),
    url(r'^logout/$',LogoutView.as_view(), name='logout'),

   

]

if settings.DEBUG:
    urlpatterns=urlpatterns + static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
    urlpatterns=urlpatterns + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)