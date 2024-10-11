from django.shortcuts import render
from django.contrib import messages
from django.urls import reverse
from django.http import HttpResponse

# Create your views here. 
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Cart, CartItem, TempraryCart, TempraryCartCartItem, WishList, WishListItem
from product.models import ProductModel, Color, SIZE, ColorSizePointer, ProductColorSize, ProductColor, ProductSize, ProductImage
from .forms import CartQuantityForm, AplyPromotion
from Shop.models import PromotionModel, UserProfile, UserPromoCode
from django.http import JsonResponse
from client.forms import NonRegesteredClientForm, ComeBackCode
from client.models import NonRegesteredClient

def aplyPromotion(request):
    if request.method == 'POST':
        promo_form = AplyPromotion(request.POST)
        if promo_form.is_valid():
            promo_code = promo_form.cleaned_data['promo_code']
            promo_codes = PromotionModel.objects.values_list('code', flat=True)
            if promo_code in promo_codes:
                try:
                    code = get_object_or_404(PromotionModel, code=promo_code)
                    if code.closed:
                        myerruer = f' Code : "{promo_code}" has expired or has been frozen'
                        return (myerruer, 0) 
                    else:
                        user_profile, created = UserProfile.objects.get_or_create(user=request.user)
                        promo, created = UserPromoCode.objects.get_or_create(user_profile=user_profile, promo_code=code)
                        if promo.used:
                            myerruer = f' Code : "{promo_code}" has expired or used !!'
                            return (myerruer, 0)
                        else:
                            promo.used = True
                            promo.save()
                            return (0, float(code.rate))
                except  promo_code.DoesNotExist as e:
                    return f'Invalid promo  "{promo_code}" or {e}'
            else:
                myerruer = f' Code : "{promo_code}"Invalid promo code'
                return (myerruer, 0)
        else:
            return ('Invalid promo code',0)
    return (0,0)                     
    
@login_required
def view_cart(request):
    message = 0
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = CartItem.objects.filter(cart=cart, is_ordered=False)
    Subtotal = sum(cart_item.subtotal for cart_item in cart_items)

    Promotion_rate = 0.0 
    if request.user.is_authenticated:
        #promo_code = request.user.profile.promo_code
        promo_rate = aplyPromotion(request)
        if isinstance(promo_rate[1], float):
            Promotion_rate = promo_rate[1]/100
        else:
            message = promo_rate[0]
            Promotion_rate = promo_rate[1]
        Promotion = float(Subtotal) * Promotion_rate
        cart.total = float(Subtotal) - float(Promotion)
        cart.save()
        Total = cart.total
        
        grooped_images = {}
        for item in cart_items:
            images = ProductImage.objects.filter(Product=item.product)
            for image in images:
                if image.color.name == item.color_size.product_color.color.name: 
                    grooped_images[item.color_size.product_color.color.name] = image.Product_Image
                    break
    else:
        Promotion = float(Subtotal) * Promotion_rate
        cart.total = float(Subtotal) - float(Promotion)
        cart.save()
        Total = cart.total
    promo_form = AplyPromotion()
    return render(request, 'cart/cartview.html', {'cart_items': cart_items, 'Subtotal':Subtotal, 'promotion':Promotion, 'Total':Total, 'promo_form':promo_form,'grooped_images':grooped_images, 'message':message})

def cart_summary(request):
    # Check if the user is authenticated
    if request.user.is_authenticated:
        cart = get_object_or_404(Cart, user=request.user)
        if cart:
            cart_items = CartItem.objects.filter(cart=cart)
            Subtotal = sum(item.subtotal for item in cart_items)
            cart.total = Subtotal
            Total = cart.total
            cart.save()
            grooped_images = {}
            for item in cart_items:
                images = ProductImage.objects.filter(Product=item.product)
                for image in images:
                    if image.color.name == item.color_size.product_color.color.name: 
                        grooped_images[item.color_size.product_color.color.name] = image.Product_Image
                        break
            # Prepare context for rendering
            context = {
                'cart_items': cart_items,
                'Subtotal': Subtotal,
                'Total': Total,
                'grooped_images':grooped_images,
            }
            return render(request, 'cart/cart_summary.html', context)
        else:
            return render(request, 'cart/cart_summary.html')

    else:
        # Handle non-registered users
        empty_cart = request.session.get('empty_cart', {})
        if empty_cart:
            cart_items = []
            total = 0

            for item_key, item_data in empty_cart.items():
                product = get_object_or_404(ProductModel, id=item_data['product_id'])
                quantity = item_data['quantity']
                color_size_data = item_data['color_size']
                color = get_object_or_404(Color, name=color_size_data['color'])
                product_color = get_object_or_404(ProductColor, product=product, color=color)
                size = get_object_or_404(SIZE, size_value=color_size_data['size'])
                color_size_pointers = get_object_or_404(ColorSizePointer, product_color=product_color)
                
                # Handle size and color size
                if len(color_size_pointers.quantities) == 1:
                    product_size = get_object_or_404(ProductSize, product=product, size=size, quantity=color_size_pointers.quantities[0])
                else:
                    product_size = next((ps for ps in color_size_pointers.quantities if ps.size == size.size_value), None)
                
                color_size = get_object_or_404(ProductColorSize, product_color=product_color, product_size=product_size)
                subtotal = quantity * product.ProductPrice
                total += subtotal
                grooped_images = {}
                cart_items.append({
                    'product': product,
                    'quantity': quantity,
                    'color_size': color_size,
                    'subtotal': subtotal,
                })
                
            for item in cart_items:
                images = ProductImage.objects.filter(Product=item['product'])
                for image in images:
                    if image.color.name == item['color_size'].product_color.color.name:                                 
                        grooped_images[image.color.name] = image.Product_Image
                        break

            # Prepare context for rendering
            context = {
                'cart_items': cart_items,
                'total': total,
                'grooped_images':grooped_images,
            }
            return render(request, 'cart/cart_summary.html', context)
        else:
            return render(request, 'cart/cart_summary.html')

@login_required
def add_to_cart(request, product_id):
    url = reverse('product:detail', kwargs={'pk': product_id})
    if request.method == 'POST':
        quantity_form = CartQuantityForm(request.POST)
        colors = request.POST.getlist('colors')
        sizes = request.POST.getlist('sizes')
        if quantity_form.is_valid() and colors and sizes:
            product = get_object_or_404(ProductModel, id=product_id)
            if product.quantity <= 0:
                return HttpResponse(status=304)
            
            product_colors = {color.name: color.id for color in product.colors.all()}
            product_sizes = {size.size_value: size.id for size in product.size.all()}
            if any(color not in product_colors for color in colors):
                return redirect(url)
            if any(size not in product_sizes for size in sizes):
                return redirect(url)
                
            color = Color.objects.get(name=colors[0])  # Assuming only one color can be selected
            size = SIZE.objects.get(size_value=sizes[0])  # Assuming only one size can be selected
            quantity = quantity_form.cleaned_data['quantity']
            cart, created = Cart.objects.get_or_create(user=request.user)
            if product.quantity >= quantity:
                product_color = get_object_or_404(ProductColor, product=product, color=color)
                
                color_size_pointers = get_object_or_404(ColorSizePointer, product_color=product_color)
                p_sizes = []
                if len(color_size_pointers.quantities) == 1:
                    product_size = get_object_or_404(ProductSize, product=product, size=size, quantity=color_size_pointers.quantities[0])
                else:
                    for quan in color_size_pointers.quantities:
                       product_size = get_object_or_404(ProductSize, product=product, size=size, quantity=quan) 
                       p_sizes.append(product_size)
                color_size, created = ProductColorSize.objects.get_or_create(
                    product_color=product_color,
                    product_size=product_size
                )
                
                cart_item = CartItem.objects.filter(
                    cart=cart,
                    product=product,
                    color_size=color_size
                ).first()

                if cart_item:
                    cart_item.quantity += quantity
                    cart_item.save()
                else:
                    cart_item = CartItem.objects.create(
                        cart=cart,
                        product=product,
                        quantity=quantity,
                        color_size=color_size
                    )
                
                product.quantity -= quantity
                product.save()
                   
            return HttpResponse(status=204) #redirect(url)
        else:
            return redirect(url)
    else:
        return redirect(url)

@login_required
def remove_from_cart(request, product_id):
    if request.method == 'POST':
        color_name = request.POST.get('color')
        size_value = request.POST.get('size')
        product = get_object_or_404(ProductModel, id=product_id)
        cart = get_object_or_404(Cart, user=request.user)
        # Get the ProductColor object
        color = get_object_or_404(Color, name=color_name)
        product_color = get_object_or_404(ProductColor, product=product, color=color)
        
        # Get the ProductSize object
        size = get_object_or_404(SIZE, size_value=size_value)
        color_size_pointers = get_object_or_404(ColorSizePointer, product_color=product_color)
                # Get the ProductSize object
        p_sizes = []
        if len(color_size_pointers.quantities) == 1:
                product_size = get_object_or_404(ProductSize, product=product, size=list(color_size_pointers.sizes.all())[0], quantity=color_size_pointers.quantities[0])
        else:
           for quan in color_size_pointers.quantities:
                product_size = get_object_or_404(ProductSize, product=product, size=list(color_size_pointers.sizes.all())[0], quantity=quan) 
                p_sizes.append(product_size)

    #    product_size = get_object_or_404(ProductSize, product=product, size=size)
        
        # Get the ProductColorSize object
        color_size = get_object_or_404(ProductColorSize, product_color=product_color, product_size=product_size)
        
        # Get the CartItem
        cart_item = get_object_or_404(CartItem, cart=cart, product=product, color_size=color_size)
        
        # Update the product's available quantity
        product.quantity += cart_item.quantity
        product.save()
        
        # Delete the CartItem
        cart_item.delete()
        
    return redirect('cart:view_cart')

@login_required
def update_cart(request, product_id, color_id):
    url = reverse('product:detail', kwargs={'pk':f'{product_id}'})
    if request.method == 'POST':
        quantity_form = CartQuantityForm(request.POST)
        if quantity_form.is_valid():
            quantity = quantity_form.cleaned_data['quantity']
            product = get_object_or_404(ProductModel, id=product_id)
            cart = get_object_or_404(Cart, user=request.user)
            color = Color.objects.get(id=color_id)
            product_color = get_object_or_404(ProductColor, product=product, color=color)
                
            color_size_pointers = get_object_or_404(ColorSizePointer, product_color=product_color)
                # Get the ProductSize object
            p_sizes = []
            if len(color_size_pointers.quantities) == 1:
                product_size = get_object_or_404(ProductSize, product=product, size=list(color_size_pointers.sizes.all())[0], quantity=color_size_pointers.quantities[0])
            else:
               for quan in color_size_pointers.quantities:
                    product_size = get_object_or_404(ProductSize, product=product, size=list(color_size_pointers.sizes.all())[0], quantity=quan) 
                    p_sizes.append(product_size)
            color_size, created = ProductColorSize.objects.get_or_create(
                    product_color=product_color,
                    product_size=product_size
                )

            cart_item = get_object_or_404(CartItem, cart=cart, product=product, color_size=color_size)
            cart_item.quantity = quantity
            cart_item.save()
            #return redirect('cart:view_cart')
            
            return HttpResponse(status=204)
        else:
            return redirect(url)
    else:
        return redirect(url)

def view_temp_cart(request):

    try:
        empty_cart = request.session.get('empty_cart', {})
        cart_id = request.session.get('cart_id', {})
        if cart_id != {}:
                cart = get_object_or_404(TempraryCart, id=cart_id)
                cart_items = TempraryCartCartItem.objects.filter(cart=cart, is_ordered=True)
                grooped_images = {}
                Total = cart.total 
                for item in cart_items:
                    Total += item.subtotal
                    images = ProductImage.objects.filter(Product=item.product)
                    for image in images:
                        if image.color.name == item.color_size.product_color.color.name: 
                            grooped_images[item.color_size.product_color.color.name] = image.Product_Image
                            break
                return render(request, 'cart/temprory_cart.html', {'cart_items': cart_items, 'Total':Total, 'grooped_images':grooped_images,})    
        elif empty_cart != {}:
                cart_items = []
                grooped_images = {}
                Total = 0
                for item_key, item_data in empty_cart.items():
                    product = ProductModel.objects.get(id=item_data['product_id'])
                    quantity = item_data['quantity']
                    color_size_data = item_data['color_size']
                    color = get_object_or_404(Color, name=color_size_data['color'])
                    product_color = get_object_or_404(ProductColor, product=product, color=color)
                    size = get_object_or_404(SIZE, size_value=color_size_data['size'])
                    color_size_pointers = get_object_or_404(ColorSizePointer, product_color=product_color)
                    p_sizes = []
                    if len(color_size_pointers.quantities) == 1:
                        product_size = get_object_or_404(ProductSize, product=product, size=size, quantity=color_size_pointers.quantities[0])
                    else:
                        for quan in color_size_pointers.quantities:
                            product_size = get_object_or_404(ProductSize, product=product, size=size, quantity=quan) 
                            p_sizes.append(product_size)
                    color_size = ProductColorSize.objects.get(product_color=product_color, product_size=product_size)
                    subtotal = quantity * product.ProductPrice
                    Total += subtotal
                    cart_item = {
                    'product': product,
                    'quantity': quantity,
                    'color_size': color_size,
                    'subtotal': subtotal
                    }
                    cart_items.append(cart_item)
                for item in cart_items:
                    images = ProductImage.objects.filter(Product=item['product'])
                    for image in images:
                        if image.color.name == item['color_size'].product_color.color.name: 
                            grooped_images[item['color_size'].product_color.color.name] = image.Product_Image
                            break
                return render(request, 'cart/temprory_cart.html', {'cart_items': cart_items, 'Total':Total, 'grooped_images':grooped_images,})
        else:
                return redirect('client:nonRegestredinformations')
    except Exception as e:
        print(e)
        return redirect('client:nonRegestredinformations')

def remove_from_temp_cart(request, product_id):
    
    if request.method == 'POST':
        color_name = request.POST.get('color')
        size_value = request.POST.get('size')
        product = get_object_or_404(ProductModel, id=product_id)
        cart_id = request.session.get('cart_id', {})
        empty_cart = request.session.get('empty_cart', {})
        if cart_id:
            cart = get_object_or_404(TempraryCart, id=cart_id)
        # Get the ProductColor object
            color = get_object_or_404(Color, name=color_name)
            product_color = get_object_or_404(ProductColor, product=product, color=color)
        # Get the ProductSize object
            size = get_object_or_404(SIZE, size_value=size_value)
            color_size_pointers = get_object_or_404(ColorSizePointer, product_color=product_color)
                # Get the ProductSize object
            p_sizes = []
            if len(color_size_pointers.quantities) == 1:
                product_size = get_object_or_404(ProductSize, product=product, size=list(color_size_pointers.sizes.all())[0], quantity=color_size_pointers.quantities[0])
            else:
                for quan in color_size_pointers.quantities:
                    product_size = get_object_or_404(ProductSize, product=product, size=list(color_size_pointers.sizes.all())[0], quantity=quan) 
                    p_sizes.append(product_size)
            color_size = get_object_or_404(ProductColorSize, product_color=product_color, product_size=product_size)
        
        # Get the CartItem
            cart_item = get_object_or_404(TempraryCartCartItem, cart=cart, product=product, color_size=color_size)
        
        # Update the product's available quantity
            product.quantity += cart_item.quantity
            product.save()
        
        # Delete the CartItem
            cart_item.delete()
        if empty_cart:
                color = request.POST.get('color')
                size = request.POST.get('size')
                product = get_object_or_404(ProductModel, id=product_id)
                items_to_remove = [key for key, item in empty_cart.items() if item['product_id'] == product_id and item['color_size']['color'] == color and item['color_size']['size'] == size]
                if items_to_remove:
                    for item_key in items_to_remove:
                        product.quantity += empty_cart[item_key]['quantity']
                        product.save()
                        del empty_cart[item_key]
                request.session['empty_cart'] = empty_cart
                messages.success(request, "Product removed from the cart.")
    #    product_size = get_object_or_404(ProductSize, product=product, size=size)        
        return redirect('cart:view_temp_cart')

def create_temp_cart(request, known_client):
    empty_cart = request.session.get('empty_cart')
    if not known_client:
        return redirect('client:nonRegestredinformations')
    
    knowen_user = NonRegesteredClient.objects.get(full_name=known_client)
    cart = TempraryCart.objects.create(user=knowen_user)
    request.session['cart_id'] = cart.id
    if empty_cart != {}:
        shekout_url = "/checkout/non_regestred_checkout/"
        return redirect(shekout_url)
    return render(request, 'cart/temprory_cart.html', {'cart': cart})

def initialize_empty_cart(request):
    if 'empty_cart' not in request.session:
        request.session['empty_cart'] = {}
    return request.session['empty_cart']

def add_to_empty_cart(request, product_id, color_size, quantity=1):
    empty_cart = initialize_empty_cart(request)

    # Serialize the color_size object
    serialized_color_size = {
        'color': color_size.product_color.color.name,
        'size': color_size.product_size.size.size_value,
    }

    # Create a unique key combining product_id and serialized color/size
    item_key = f"{product_id}-{serialized_color_size['color']}-{serialized_color_size['size']}"

    if item_key in empty_cart:
        empty_cart[item_key]['quantity'] += quantity
    else:
        empty_cart[item_key] = {
            'product_id': product_id,
            'quantity': quantity,
            'color_size': serialized_color_size
        }
    return request.session['empty_cart']

def add_to_temp_cart(request, product_id):
    url = reverse('product:detail', kwargs={'pk': product_id})
    if request.method == 'POST':
        quantity_form = CartQuantityForm(request.POST)
        colors = request.POST.getlist('colors')
        sizes = request.POST.getlist('sizes')
        if quantity_form.is_valid() and colors and sizes:
            product = get_object_or_404(ProductModel, id=product_id)
            
            if product.quantity <= 0:
                return HttpResponse(status=304)
            
            product_colors = {color.name: color.id for color in product.colors.all()}
            product_sizes = {size.size_value: size.id for size in product.size.all()}

            if any(color not in product_colors for color in colors):
                return redirect(url)
            if any(size not in product_sizes for size in sizes):
                return redirect(url)

            color = Color.objects.get(name=colors[0])  # Assuming only one color can be selected
            size = SIZE.objects.get(size_value=sizes[0])  # Assuming only one size can be selected
            quantity = quantity_form.cleaned_data['quantity']
            cart_id = request.session.get('cart_id')
            if product.quantity >= quantity:
                product_color = get_object_or_404(ProductColor, product=product, color=color)
                
                color_size_pointers = get_object_or_404(ColorSizePointer, product_color=product_color)
                p_sizes = []
                if len(color_size_pointers.quantities) == 1:
                    product_size = get_object_or_404(ProductSize, product=product, size=size, quantity=color_size_pointers.quantities[0])
                else:
                    for quan in color_size_pointers.quantities:
                       product_size = get_object_or_404(ProductSize, product=product, size=size, quantity=quan) 
                       p_sizes.append(product_size)
                color_size, created = ProductColorSize.objects.get_or_create(
                    product_color=product_color,
                    product_size=product_size
                )
            if not cart_id or cart_id == {}:
                cart = add_to_empty_cart(request=request, product_id=product_id, color_size=color_size, quantity=quantity)
                product.quantity -= quantity
                product.save()
            else:
                cart = get_object_or_404(TempraryCart, id=cart_id)
                cart_item = TempraryCartCartItem.objects.filter(
                    cart=cart,
                    product=product,
                    color_size=color_size
                ).first()

                if cart_item:
                    cart_item.quantity += quantity
                    cart_item.save()
                else:
                    cart_item = TempraryCartCartItem.objects.create(
                        cart=cart,
                        product=product,
                        quantity=quantity,
                        color_size=color_size
                    )
                
                product.quantity -= quantity
                product.save()
                   
            return HttpResponse(status=204)
        else:
            return redirect(url)
    else:
        return redirect(url)
   # return render(request, 'item_added.html', {'cart': cart})

@login_required
def finalize_order(request):
    cart_id = request.session.get('cart_id')
    if not cart_id:
        return render(request, 'error.html', {'message': 'Cart not found'})
    cart = get_object_or_404(Cart, id=cart_id)
    url = "/cart/"
    success_url = f"{reverse('core:success')}?redirect_url={url}"
    return redirect(success_url)

def finalize_non_order(request):
    cart_id = request.session.get('cart_id')
    empty_cart = request.session.get('empty_cart')
    
    if not cart_id:
        return render(request, 'error.html', {'message': 'Cart not found'})
    cart = get_object_or_404(TempraryCart, id=cart_id)
    url = "/cart/view_temp_cart/"
    if not empty_cart:
        return redirect(url)
    else:
        success_url = f"{reverse('core:success')}?redirect_url={url}"
        return redirect(success_url)
    
def unknown_client_options(request):
    if request.method == 'POST':
        comback_form = ComeBackCode(request.POST)
        if comback_form.is_valid():
            client_identifier = comback_form.cleaned_data['comeback_code']
            try:
                now_known_client = NonRegesteredClient.objects.get(comeback_code=client_identifier)
                return redirect('cart:create_temp_cart', client_id=now_known_client.id)
            except NonRegesteredClient.DoesNotExist:
                message = f'Unknown code {client_identifier}. Please verify or look at options below.'
                return render(request, 'cart/options_for_unregestred.html', {'form': comback_form, 'message': message})
        else:
            message = 'Invalid form submission. Please correct the errors below.'
            return render(request, 'cart/options_for_unregestred.html', {'form': comback_form, 'message': message})
    else:
        comback_form = ComeBackCode()
        return render(request, 'cart/options_for_unregestred.html', {'form': comback_form, 'message': ''})

def view_wish_list(request):
    grooped_images = {}
    if request.user.is_authenticated:
        wishlist = get_object_or_404(WishList,user=request.user)
        wishlist_items = WishListItem.objects.filter(wish_list=wishlist)

    else:
        wishlist_items = []
        wishlist_session = request.session.get('wishlist', [])
        for item in wishlist_session:
            try:
                product = ProductModel.objects.get(id=item)
                wishlist_items.append({'product': product})

            except ProductModel.DoesNotExist:
                continue

    return render(request, 'cart/view_wish_list.html', {'wishlist_items': wishlist_items})

def wish_list_summary(request):
    grooped_images = {}
    if request.user.is_authenticated:
        wishlist = get_object_or_404(WishList,user=request.user)
        wishlist_items = WishListItem.objects.filter(wish_list=wishlist)
        for item in wishlist_items:
            images = ProductImage.objects.filter(Product=item.product)
            for image in images:
                if image.color.name == item.product.colors.all().first().name:
                    grooped_images[item.product.colors.all().first()] = image.Product_Image
                    break
    else:
        wishlist_items = []
        wishlist_session = request.session.get('wishlist', [])
        for item in wishlist_session:
            try:
                product = ProductModel.objects.get(id=item)
                wishlist_items.append({'product': product})
                
                for item in wishlist_items:
                    images = ProductImage.objects.filter(Product=item['product'])
                    for image in images:
                        if image.color.name == product.colors.name: 
                            grooped_images[image.color.name] = image.Product_Image
                            break
            except ProductModel.DoesNotExist:
                continue
    return render(request, 'cart/wish_list_summary.html', {'wishlist_items': wishlist_items, 'grooped_images':grooped_images})

def add_wish_list(request, product_id):
    product = get_object_or_404(ProductModel, id=product_id)
    if request.user.is_authenticated:
        wishlist, created = WishList.objects.get_or_create(user=request.user)
        WishListItem.objects.get_or_create(wish_list=wishlist, product=product)

    else:
        wishlist_session = request.session.get('wishlist', [])
        if product_id not in wishlist_session:
            wishlist_session.append(product_id)
            request.session['wishlist'] = wishlist_session
    return HttpResponse(status=204)

def remove_wish_list(request, product_id):
    if request.user.is_authenticated:
        wishlist = WishList.objects.get(user=request.user)
        WishListItem.objects.filter(wish_list=wishlist, product_id=product_id).delete()
    else:
        wishlist_session = request.session.get('wishlist', [])
        if product_id in wishlist_session:
            wishlist_session.remove(product_id)
            request.session['wishlist'] = wishlist_session

    return redirect('cart:view_wish_list')
