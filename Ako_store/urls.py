"""
URL configuration for Ako_store project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('receipt/', include('receipt.urls')),
    path('products/', include('product.urls')),
    path('client/', include('client.urls')),
    path('cart/', include('cart.urls')),
    path('order/', include('order.urls')),
    path('checkout/', include('checkout.urls')),
    path('shop/', include('Shop.urls')),
    path('shopTools/', include('ShopTools.urls')),
    path('', include('core.urls')),
    path('headline/', include('headline.urls')),
    path('search/', include('search.urls')),
    path('review/', include('reviews.urls')),
    path('filter/', include('filtter.urls')),
    path('admin/', admin.site.urls),
]