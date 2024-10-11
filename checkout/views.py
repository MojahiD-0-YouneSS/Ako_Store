from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from cart.models import Cart, CartItem, TempraryCart, TempraryCartCartItem
from shopingHistory.models import ShoppingHistory, NonRegestredShoppingHistory
from order.models import Order, OrderItem, NonRegestredOrder, NonRegestredOrderItem, ShippingAddress, ShippingNonAddress
from client.models import Client, NonRegesteredClient
from product.models import ProductModel, Color, SIZE, ProductColor, ProductSize, ProductColorSize, ColorSizePointer
from django.urls import reverse

@login_required
def checkout(request):
    cart = get_object_or_404(Cart, user=request.user)
    regestred_user = get_object_or_404(Client, email=request.user.email)
    shipping_address, created = ShippingAddress.objects.get_or_create(user=regestred_user, full_name=regestred_user.full_name, address_line_1=regestred_user.address, city=regestred_user.city, phone_number=regestred_user.phone)
    if  not regestred_user.address and not regestred_user.city and not regestred_user.full_name and not regestred_user.phone:
        message = "fill up your informtion !!"
        return redirect('client:informations')

    if CartItem.objects.filter(cart=cart).exists():
        order = Order.objects.create(user=request.user, status='Pending', shipping_address=shipping_address, total=cart.total)
        for item in CartItem.objects.filter(cart=cart):
            OrderItem.objects.create(order=order, product=item.product, quantity=item.quantity, subtotal=item.subtotal)
            item.is_ordered = True
        cart.save()
        history, created = ShoppingHistory.objects.get_or_create(user=request.user)
        history.orders.add(order)
        return redirect('cart:finalize_order')
    return redirect('cart:view_cart')

def non_regestred_checkout(request):
    cart_id = request.session.get('cart_id', {})
    empty_cart = request.session.get('empty_cart', {})
    if cart_id and cart_id != {} and empty_cart == {}:
        cart = get_object_or_404(TempraryCart, id=cart_id)
        nonregestred_user = get_object_or_404(NonRegesteredClient, full_name=cart.user.full_name,)
    
        if  not nonregestred_user.address and not nonregestred_user.city and not nonregestred_user.full_name and not nonregestred_user.phone:
            message = "fill up your informtion !!"
            return redirect('client:nonRegestredinformations')

        if TempraryCartCartItem.objects.filter(cart=cart).exists():
            order = NonRegestredOrder.objects.create(user=nonregestred_user, status='Pending', total=cart.total)
            for item in TempraryCartCartItem.objects.filter(cart=cart):
                NonRegestredOrderItem.objects.create(order=order, product=item.product, quantity=item.quantity, subtotal=item.subtotal)
                item.is_ordered = True
                cart.save()
                history, created = NonRegestredShoppingHistory.objects.get_or_create(user=nonregestred_user)
                history.orders.add(order)
            return redirect('cart:finalize_non_order')
    elif empty_cart and empty_cart != {}:
                user_name = request.session.get('user_name', {})
                
                if user_name == {} and cart_id == {}:
                    return redirect('client:nonRegestredinformations')
                cart_items = []
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
                temp_cart = get_object_or_404(TempraryCart, id=cart_id)
                for item in cart_items:
                    TempraryCartCartItem.objects.create(
                        cart=temp_cart,
                        product=item['product'],
                        quantity=item['quantity'],
                        color_size = item['color_size'],
                        subtotal=item['subtotal']
                        )
                user = get_object_or_404(NonRegesteredClient, full_name=user_name)
                order = NonRegestredOrder.objects.create(user=user, status='Pending', total=temp_cart.total)
                for item in TempraryCartCartItem.objects.filter(cart=temp_cart):
                    NonRegestredOrderItem.objects.create(order=order, product=item.product, quantity=item.quantity, subtotal=item.subtotal)
                    item.is_ordered = True
                    temp_cart.save()
                    history, created = NonRegestredShoppingHistory.objects.get_or_create(user=user)
                    history.orders.add(order)
                request.session['empty_cart'] = {}
                return redirect('cart:finalize_non_order')
    return redirect('cart:view_temp_cart')
