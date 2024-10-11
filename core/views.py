from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.views import LogoutView
from .forms import SignupForm
from product.models import ProductModel, ProductImage, ProductTags
from client.views import client_email_handler
# Create your views here.
 
def index(request):
    items = ProductModel.objects.all()
    item_images = ProductImage.objects.all()
    items_tags = ProductTags.objects.all()
    client_email_handler()
    return render(request, 'core/index.html', {'items':items, 'tags':items_tags, 'item_images':item_images})

def welcome(request):
    return render(request, 'core/welcome.html')
def base(request):
    return render(request, 'core/base.html')

def success(request):
    redirect_url = request.GET.get('redirect_url', '/cart/')
    return render(request, 'infos/success.html', {'redirect_url': redirect_url})

def shop_success(request):
    redirect_url = request.GET.get('redirect_url', '/')
    return render(request, 'infos/shop_success.html', {'redirect_url': redirect_url})

def contact(request):
    return render(request, 'core/contact.html')

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        
        if form.is_valid():
            form.save()
            
            return redirect('/login/')
    else:
        form = SignupForm()
    return render(request, 'core/signup.html', {
        'form' : form
    })

class CustomLogoutView(LogoutView):
    def dispatch(self, request, *args, **kwargs):
        if request.method == 'GET':
            logout(request)
            return redirect('/login/')  # Redirect to home page after logout
        return super().dispatch(request, *args, **kwargs)

