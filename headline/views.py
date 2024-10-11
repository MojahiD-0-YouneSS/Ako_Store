from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from product.models import ProductModel, ProductCategory, ProductCategoryParent,ProductColorSize, ProductColor, ProductSize, ColorSizePointer
from django.contrib.auth.models import User

from cart.models import CartItem, Cart
from .forms import AdvertizingForm
from .models import AdvertizmentHeadline, HeadlinedProduct
# Create your views here.

def ProductHeadline(request):
    headlinedProduct = ProductModel.objects.filter(headding=True)
    return render(request,'headline/headliner.html', {'hedlined':headlinedProduct,})

def TopWearHeadline(request):
    categoryT = ProductCategoryParent.objects.get(ProductCategoryP='Top')
    Top_headlinedProduct = ProductModel.objects.filter(ProductCategoriesParent=categoryT.id)
    categoryD = ProductCategoryParent.objects.get(ProductCategoryP='Down')
    Down_headlinedProduct = ProductModel.objects.filter(ProductCategoriesParent=categoryD.id)
  
    categoryF = ProductCategoryParent.objects.get(ProductCategoryP='Feet')
    Feet_headlinedProduct = ProductModel.objects.filter(ProductCategoriesParent=categoryF.id)
    context = {'Top_headlinedProduct':Top_headlinedProduct,'Down_headlinedProduct':Down_headlinedProduct, 'Feet_headlinedProduct':Feet_headlinedProduct,}
    return render(request,'headline/headliner.html', context)

def clientAds(request):
    ads = AdvertizmentHeadline.objects.all()
    maper = {}
    for ad in ads:
        if ad.for_product:
            maper[ad.product_number] = ProductModel.objects.get(reference_number=ad.product_number)
    return render(request,'headline/ads_shower.html', {'ads':ads, 'maper':maper})

def Advertaisment(request):
    if request.method == 'POST':
        ads_form = AdvertizingForm(request.POST, request.FILES)
        if ads_form.is_valid():
            advertisment = ads_form.save(commit=False)
            if advertisment.for_product:
                product = ProductModel.objects.get(reference_number=advertisment.product_number)
            advertisment.save()
            return redirect('headline:advertizment')
        else:
            return render(request, 'headline/advertizer.html', {'ads_form':ads_form})
    else:
        ads_form = AdvertizingForm()
    return render(request, 'headline/advertizer.html', {'ads_form':ads_form})

def ads_list(request):
    ads = AdvertizmentHeadline.objects.all()
    return render(request, 'headline/ads_list.html', {'ads': ads}) 

def Delete_Advertisment(request, ad_id):
    ad = get_object_or_404(AdvertizmentHeadline, id=ad_id)
    ad.delete()
    return redirect('headline:ads_list')

def outfit_selector(request, topwareref, legwareref, feetwareref, usr):
    user = get_object_or_404(User, username=usr)
    topware = get_object_or_404(ProductModel, reference_number=topwareref)
    legware = get_object_or_404(ProductModel, reference_number=legwareref)
    feetware = get_object_or_404(ProductModel, reference_number=feetwareref)
    cart = get_object_or_404(Cart,user=user.id)
    def add_product_to_cart(cart, product):
        product_color = ProductColor.objects.filter(product=product, color=product.colors.first()).first()
        #colors_sizes = ColorSizePointer.objects.filter(product=product_color, color=product_color.color)
        #product_siwe = ProductSize.objects.filter(product=product, color=product.sizes.first())
        color_sizes = get_list_or_404(ProductColorSize, product_color=product_color)
        try:
            cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product, color_size=color_sizes[0])
            if not created:
                cart_item.quantity += 1
            cart_item.save()
        
        except CartItem.MultipleObjectsReturned:
            cart_items = CartItem.objects.filter(cart=cart, product=product, color_size=color_sizes[0])
            cart_item = cart_items.first()
            cart_item.quantity += 1
            cart_item.save()
            cart_items.exclude(id=cart_item.id).delete()

    add_product_to_cart(cart, topware)
    add_product_to_cart(cart, legware)
    add_product_to_cart(cart, feetware)
    return redirect('cart:view_cart')

def ProductTagsHeadline(request):
    products = ProductModel.objects.all()
    new_headlinedProduct = products.filter(ProductTagsList__New=True).distinct()
    limitted_headlinedProduct = products.filter(ProductTagsList__Limited=True).distinct()
    
    return render(request,'headline/tagsheadliner.html', {'New':'NEW', 'Limitted':'LIMITTED', 'new_hedlined':new_headlinedProduct,'limited_hedlined':limitted_headlinedProduct,})
