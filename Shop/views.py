from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
import random
import string
from datetime import datetime
from django.views import View
from .forms import ProductFinderForm, DropdownForm, PromotionForm, FreezUnFreezPromotion, PosterForm
from .models import PromotionModel, UserProfile, UserPromoCode, ShopPoster
from client.models import Client, NonRegesteredClient
from product.models import ProductFabric, FabricModel, ProductModel, ProductCategory, ProductCategoryChild, ProductCategoryParent, ProductColor, ProductImage, ProductSize
from product.forms import ProductFabricForm
from django.core.exceptions import ValidationError
from reviews.models import BannedUser, BannedNonUser
from django.http import JsonResponse
from django.contrib.auth.models import User
from cart.models import Cart, CartItem, TempraryCart, TempraryCartCartItem
from order.models import Order, OrderItem, CancelledNonOrder, CancelledNonOrderItem, CancelledOrder,CancelledOrderItem, NonRegestredOrder, NonRegestredOrderItem, ValidNonOrder, ValidNonOrderItem, ValidOrder, ValidOrderItem
# Create your views here.
def shopInterface(request):
    return render(request, 'shop/shopenterface.html')

def process_selected_element(selected_element):
    selected_element= '*********\\___/*********'
    return HttpResponse(f'Selected element: {selected_element}')

def DropDownSelectOption(request):
    if request.method == 'POST':
        form = DropdownForm(request.POST)
        if form.is_valid():
            selected_element = form.cleaned_data['element']
            return process_selected_element(selected_element)
    else:
        form = DropdownForm()
    return render(request, 'shop/dropDownTemplate.html', {'form': form})

class ProductDetailView(View):
    def get(self, request, *args, **kwargs):
        form = ProductFinderForm()
        products = ProductModel.objects.all()
        return render(request, 'shop/detail_finder.html', {'form': form, 'products': products})

    def post(self, request, *args, **kwargs):
        form = ProductFinderForm(request.POST)
        products = ProductModel.objects.all()
        if form.is_valid():
            if form.cleaned_data['element'] == 'id':
                input_data = form.cleaned_data['input_data']
                try:
                    products = ProductModel.objects.get(id=input_data)
                except:
                    products = None
                return render(request, 'shop/detail_finder.html', {'form': form, 'products':[products],})
            else:
                element_shosen = form.cleaned_data['element']
                input_data = form.cleaned_data['input_data']
                if element_shosen == 'category parent':
                    category = get_object_or_404(ProductCategoryParent, ProductCategoryP=input_data)
                    products = ProductCategory.objects.filter(main_category=category.id)
                    return render(request, 'shop/detail_finder.html', {'form': form, 'products':products,})
                elif element_shosen == 'category child':
                    try:
                        category = ProductCategoryChild.objects.get(ProductCategoryC=input_data)
                        products = ProductCategory.objects.filter(sub_category=category.id)
                    except:
                        products = None
                    return render(request, 'shop/detail_finder.html', {'form': form, 'products':products,})
        return render(request, 'shop/detail_finder.html', {'form': form, 'products':products,})

def ProductDetailInterface(request):
    return render(request, 'shop/detail_finder.html')

def delete_all_products(request):
    #ProductModel.objects.all().delete()
    return redirect('core:success')

def generate_random_code():
    length=10
    alphanumeric_chars = string.ascii_letters + string.digits
    return ''.join(random.choice(alphanumeric_chars) for _ in range(length))

def get_promo_code(request):
    if request.method == 'GET':
        promo_code = generate_random_code()
        return JsonResponse({'promo_code': promo_code})
    return JsonResponse({'error': 'Invalid request method'}, status=400)

def PromotionCode(request):
    hello = 0
    message = None
    if request.method == 'POST':
        promotion_form = PromotionForm(request.POST)
        freez_form = FreezUnFreezPromotion(request.POST)
        if freez_form.is_valid():
            promo_code = freez_form.cleaned_data['promotion_code']
            codes = PromotionModel.objects.values_list('code', flat=True)
            if promo_code in codes:
                target = PromotionModel.objects.filter(code=promo_code)
                if not target.closed:
                    target.closed = True
                    message = {'message':'promotion code is freezed', 'status':1}
                else:
                    target.closed = False
                    message = {'message':'promotion code is unfreezed', 'status':0}
            else:
                message = "promotion code don't exist"
        if promotion_form.is_valid():
            rate = promotion_form.cleaned_data['rate']
            if rate <= 100:
                promotion = promotion_form.save(commit=False)
                promotion.code = request.POST.get('promo_code', generate_random_code())
                promotion.save()
                return redirect('shop:promotion')
            else:
                hello = f"use rate 0 - 100 not {rate}"
                print(hello)
    else:
        promotion_form = PromotionForm()
        freez_form = FreezUnFreezPromotion()
        
    promotion_codes = PromotionModel.objects.all()
    initial_promo_code = generate_random_code()
    return render(request, 'shop/promotion.html', {
        'promotion_form': promotion_form, 
        'initial_promo_code': initial_promo_code, 
        'promotion_codes': promotion_codes, 
        'myerreur':hello,
        'message':message,
        'freez_form':freez_form,})

def freezUnfreezCode(request, promo_code):
    code = get_object_or_404(PromotionModel, code=promo_code)
    code.closed = not code.closed
    code.save()
    status_message = 'frozen' if code.closed else 'unfrozen'
    return JsonResponse({'message': f'Promotion code is {status_message}', 'status': code.closed})

def regestred_users(request):
    try:
        # Exclude users with the username 'admin' and 'owner'
        users = User.objects.exclude(username='ILiac_Ak0') #.exclude(username='admin')
        # Prepare user data to return
        user_data = []
        for user in users:
            user_info = {
                'username': user.username,
                'is_active': user.is_active,
                # Add other fields if necessary
            }
            user_data.append(user_info)
        return render(request, 'shop/regestered_clients.html',{'users': user_data})

    except Exception as e:
        return render(request, 'shop/regestered_clients.html', {'mssg':e})
 
def nonuserinfo(request, user_id):
    
    try:
        user = get_object_or_404(NonRegesteredClient, id=user_id)
        TempraryCart.objects.get(user=user)
    except:
        TempraryCart.objects.get_or_create(user=user)

    
    try:
        # Fetch the user, user profile, user promo codes, and user cart
        user = get_object_or_404(NonRegesteredClient, id=user_id)
        the_cart = get_object_or_404(TempraryCart, user=user)
        user_cart_items = TempraryCartCartItem.objects.filter(cart=the_cart)  # Retrieve all items in the user's cart

        if user.is_active:
            last_seen = datetime.now().strftime('%Y/%m/%d _ %H:%M:%S')
        else:
            last_seen = 'still working on it !!'
        orders = NonRegestredOrder.objects.filter(user=user)
        total_order_items = []
        total_cancelled_order_items = []
        total_validated_items = []
        for order in orders:
            order_items = NonRegestredOrderItem.objects.filter(order=order)
            total_order_items += order_items
            if order.is_canceled:
                canceled_order = get_object_or_404(CancelledNonOrder, original_order_object=order)
                cancelled_items = CancelledNonOrderItem.objects.filter(cancelled_order=canceled_order)
                total_cancelled_order_items += cancelled_items
            if order.is_validated:
                validated_order = get_object_or_404(ValidNonOrder, original_order_object=order)
                validated_items = ValidNonOrderItem.objects.filter(validated_order=validated_order)
                total_validated_items += validated_items              
        return render(request, 'shop/user_info.html', {
            'user_info':user,
            'cart': the_cart,
            'cart_items': user_cart_items,
            'last_seen': last_seen,
            'cart_items': user_cart_items,
            'total_order_items':total_order_items,
            'total_cancelled_order_items':total_cancelled_order_items,
            'total_validated_items':total_validated_items,
        })
        
    except Exception as e:
        print(e)
        return render(request, 'shop/user_info.html')
 
def userinfo(request, username):
    try:
        user = get_object_or_404(User, username=username)
        user_profile = get_object_or_404(UserProfile, user=user)
        user_promos = UserPromoCode.objects.filter(user_profile=user_profile)  # Retrieve promo codes associated with the user profile
        the_cart = get_object_or_404(Cart, user=user)
        user_cart_items = CartItem.objects.filter(cart=the_cart)  # Retrieve all items in the user's cart
        if user_profile.user.is_active:
            last_seen = datetime.now().strftime('%Y/%m/%d _ %H:%M:%S')
        else:
            last_seen = 'still working on it !!'
        orders = Order.objects.filter(user=user)
        total_order_items = []
        total_cancelled_order_items = []
        total_validated_items = []
        for order in orders:
            order_items = OrderItem.objects.filter(order=order)
            total_order_items += order_items
            if order.is_canceled:
                canceled_order = get_object_or_404(CancelledOrder, original_order_object=order)
                cancelled_items = CancelledOrderItem.objects.filter(cancelled_order=canceled_order)
                total_cancelled_order_items += cancelled_items
            if order.is_validated:
                validated_order = get_object_or_404(ValidOrder, original_order_object=order)
                validated_items = ValidOrderItem.objects.filter(validated_order=validated_order)
                total_validated_items += validated_items              
        return render(request, 'shop/user_info.html', {
            'promotions': user_promos,
            'cart': the_cart,
            'user_profile': user_profile,
            'last_seen': last_seen,
            'cart_items': user_cart_items,
            'total_order_items':total_order_items,
            'total_cancelled_order_items':total_cancelled_order_items,
            'total_validated_items':total_validated_items,
        })
    except Exception as e:
        return render(request, 'shop/user_info.html')


def product_view(request):
    # Get all product category parents
    category_parents = ProductCategoryParent.objects.all()
    
    # Initialize a dictionary to hold grouped images by category and color
    grouped_images = {}

    for category in category_parents:
        # Get all products for the current category parent
        products = ProductModel.objects.filter(ProductCategoriesParent=category)
        grouped_images[category.ProductCategoryP] = {}

        for product in products:
            for color in product.colors.all():
                if color.name not in grouped_images[category.ProductCategoryP]:
                    grouped_images[category.ProductCategoryP][color.name] = []
                
                for image in product.images.filter(color=color):
                    grouped_images[category.ProductCategoryP][color.name].append(image.Product_Image.url)
    
    context = {
        'grouped_images': grouped_images,
    }
    return render(request, 'shop/product_gallery.html', context)

def poster_uploader(request):
    if request.method == 'POST':
        poster_form = PosterForm(request.POST)
        if poster_form.is_valid():
            poster_form.save()
            return redirect('shop:shopInterface')
    else:
        poster_form = PosterForm()
        return render(request, 'shop/poster_form.html', {'form':poster_form})
    
def poster_setter(request):
    return render(request, 'shop/poster.html')

def fabric_adder(request):
    if request.method == 'POST':
        fabric_form = ProductFabricForm(request.POST)
        if fabric_form.is_valid():
            product_ref = fabric_form.cleaned_data['product']
            fabric = fabric_form.cleaned_data['fabric']
            pure = fabric_form.cleaned_data['pure']
            if pure:
                fabric_obj, created = FabricModel.objects.get_or_create(name=fabric)
                if created:
                    product = get_object_or_404(ProductModel, reference_number=product_ref)
                    ProductFabric.objects.create(product=product, pure=pure, fabric=fabric_obj.name)
                return redirect('shop:fabric_adder')
            else:
                fabric_names = []
                L1_fabric_comb = fabric.split('\n')
                for x in L1_fabric_comb:
                    try:
                        name = x.split(' ', 1)[1].strip()  # Extract the fabric name
                        fabric_names.append(name)
                    except IndexError:
                        print("Invalid fabric format. Ensure each line follows the format '<percentage> <fabricName>'.")
                        return redirect('shop:fabric_adder')

                for name in fabric_names:
                    FabricModel.objects.get_or_create(name=name)

                product = get_object_or_404(ProductModel, reference_number=product_ref)
                ProductFabric.objects.create(product=product, pure=pure, fabric=fabric)
                return redirect('shop:fabric_adder')
        else:
            form = ProductFabricForm()
            return render(request, 'shop/fabric.html', {'form':form})
    else:
        form = ProductFabricForm()
        return render(request, 'shop/fabric.html', {'form':form})

def banned_users(request):
    banned_users_infos = BannedUser.objects.all()
    return render(request, 'shop/banned_user_list.html', {'users':banned_users_infos})

def users_without_acounts(request):
    users_infos = NonRegesteredClient.objects.all()
    return render(request, 'shop/non_user_list.html', {'users':users_infos})

def banned_users_without_acounts(request):
    banned_users = BannedNonUser.objects.all()
    return render(request, 'shop/banned_non_user_list.html', {'users':banned_users})

