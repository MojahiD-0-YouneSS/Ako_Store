from django.shortcuts import render
from django.contrib.auth.models import User
# Create your views here..
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Order, OrderItem, NonRegestredOrder, NonRegestredOrderItem, CancelledOrder, CancelledOrderItem, CancelledNonOrder, CancelledNonOrderItem, ValidNonOrder, ValidNonOrderItem, ValidOrder, ValidOrderItem
from django.db.models import Q
from django.http import JsonResponse, HttpResponse
from client.models import Client, NonRegesteredClient
from product.models import ProductModel

@login_required
def user_orders_view(request, user_id):
    user = get_object_or_404(User, id=user_id)
    orders = Order.objects.filter(user=user, is_canceled=False)
    return render(request, 'order/user_orders.html', {'orders': orders, 'user': user})

@login_required
def list_all_orders(request):
    users = User.objects.all()
    
    users_orders = []
    for user in users:
        orders = Order.objects.filter(user=user, is_canceled=False)
        users_orders.append({'user': user, 'orders': orders})
        
    return render(request, 'order/users_and_orders.html', {'users_orders': users_orders})

@login_required
def nonlist_all(request):
    users = NonRegesteredClient.objects.all().distinct()
    users_orders = []
    for user in users:
        orders = NonRegestredOrder.objects.filter(user=user, is_canceled=False)
        users_orders.append({'user': user, 'orders': orders})

    return render(request, 'order/non_users_and_orders.html', {'users_orders': users_orders})

def non_order_detail_view(request, order_id):
    order = get_object_or_404(NonRegestredOrder, id=order_id)
    order_items = NonRegestredOrderItem.objects.filter(order=order)
    total = sum([x.product.ProductPrice * x.quantity for x in order_items])
    subtotal_per_product =  [
    {'item': x, 'subtotal': x.product.ProductPrice * x.quantity}
    for x in order_items
    ]
    shipping_info = NonRegesteredClient.objects.filter(address=order.user.address).first()
    return render(request, 'order/non_client_order_detail.html', {'order': order, 'shipping_info': shipping_info, 'total':total, 'product_cost':subtotal_per_product})

@login_required
def order_detail_view(request, order_id):
    order = get_object_or_404(Order, id=order_id, is_canceled=False)
    order_items = OrderItem.objects.filter(order=order)
    total = sum([x.product.ProductPrice * x.quantity for x in order_items])
    subtotal_per_product =  [
    {'item': x, 'subtotal': x.product.ProductPrice * x.quantity}
    for x in order_items
    ]
    shipping_info = Client.objects.get(email=order.user.email)
    return render(request, 'order/client_order_detail.html', {'order': order, 'shipping_info': shipping_info, 'total':total, 'product_cost':subtotal_per_product})

@login_required
def shop_non_order_detail_view(request, order_id):
    order = get_object_or_404(NonRegestredOrder, id=order_id)
    order_items = NonRegestredOrderItem.objects.filter(order=order)
    total = sum([x.product.ProductPrice * x.quantity for x in order_items])
    subtotal_per_product =  [
    {'item': x, 'subtotal': x.product.ProductPrice * x.quantity}
    for x in order_items
    ]
    shipping_info = NonRegesteredClient.objects.filter(address=order.user.address).first()
    return render(request, 'order/non_order_detail.html', {'order': order, 'shipping_info': shipping_info, 'total':total, 'product_cost':subtotal_per_product})

@login_required
def canceled_order_detail_view(request, order_id):
    order = get_object_or_404(CancelledOrder, id=order_id)
    order_items = CancelledOrderItem.objects.filter(cancelled_order=order)
    total = sum([x.product.ProductPrice * x.quantity for x in order_items])
    origenal_order = get_object_or_404(Order, id=order.original_order_id)
    subtotal_per_product =  [
    {'item': x, 'subtotal': x.product.ProductPrice * x.quantity}
    for x in order_items
    ]
    shipping_info = Client.objects.get(email=order.user.email)
    return render(request, 'order/cannceled_order_details.html', {'order': origenal_order, 'shipping_info': shipping_info, 'total':total, 'product_cost':subtotal_per_product, 'canceled_order':order})

@login_required
def shop_order_detail_view(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order_items = OrderItem.objects.filter(order=order)
    total = sum([x.product.ProductPrice * x.quantity for x in order_items])
    subtotal_per_product =  [
    {'item': x, 'subtotal': x.product.ProductPrice * x.quantity}
    for x in order_items
    ]
    shipping_info = Client.objects.get(email=order.user.email)
    return render(request, 'order/order_detail.html', {'order': order, 'shipping_info': shipping_info, 'total':total, 'product_cost':subtotal_per_product})

@login_required
def pending_orders_view(request):
    pending_orders = Order.objects.filter(status='Pending', is_canceled=False)
    return render(request, 'order/pending_orders.html', {'pending_orders': pending_orders})

@login_required
def update_order_status_view(request, order_id, user_email):
    order = get_object_or_404(Order, id=order_id, status='Pending')
    email = get_object_or_404(User, email=user_email)
    if order.products.count() > 0:
        order.status = 'Ready to Ship'
        order.save()
        message = 'Order updated to Ready to Ship'
    else:
        message = 'Order not ready to ship: No products in order'
    return render(request, 'order/update_order_status.html', {'order': order, 'message': message, 'email':email})

def cancel_order_items(order_model, order_item_model, identifier):
    if order_model == Order:
        order = get_object_or_404(order_model, id=identifier)
        cancelled_order, created = CancelledOrder.objects.get_or_create(user=order.user, original_order_id=order.id, original_order_object= order)
    
        order_items = order_item_model.objects.filter(order=order)

        for item in order_items:
            CancelledOrderItem.objects.create(cancelled_order=cancelled_order, product=item.product, quantity=item.quantity, price_at_cancellation=item.product.ProductPrice)
            product = get_object_or_404(ProductModel, id=item.product.id)
            product.quantity += item.quantity
            product.save()
    else:
        order = get_object_or_404(order_model, id=identifier)
        cancelled_order, created = CancelledNonOrder.objects.get_or_create(user=order.user, original_order_id=order.id, original_order_object= order)

        order_items = order_item_model.objects.filter(order=order)

        for item in order_items:
            CancelledNonOrderItem.objects.create(cancelled_order=cancelled_order, product=item.product, quantity=item.quantity, price_at_cancellation=item.product.ProductPrice)
            product = get_object_or_404(ProductModel, id=item.product.id)
            product.quantity += item.quantity
            product.save()

    order.is_canceled = True
    order.save()
    return order

@login_required
def cancel_order(request, order_id):
    cancel_order_items(Order, OrderItem, order_id)
    return redirect('order:pending')

@login_required
def cancel_non_order(request, order_id):
    cancel_order_items(NonRegestredOrder, NonRegestredOrderItem, order_id)
    return redirect('order:nonlist_all')

@login_required
def non_canceled_order_detail(request, order_id):
    cancelled_order = CancelledNonOrder.objects.get(id=order_id)
    cancelled_orders_items = CancelledNonOrderItem.objects.filter(cancelled_order=cancelled_order)
    total = sum([x.product.ProductPrice * x.quantity for x in cancelled_orders_items])
    origenal_order = get_object_or_404(NonRegestredOrder, id=cancelled_order.original_order_id, is_canceled=True)
    subtotal_per_product =  [
    {'item': x, 'subtotal': x.product.ProductPrice * x.quantity}
    for x in cancelled_orders_items
    ]
    shipping_info = NonRegesteredClient.objects.get(phone=cancelled_order.user.phone)
    return render(request, 'shoppingHistory/non_canceled_orders_detail.html', {'order': origenal_order, 'shipping_info': shipping_info, 'total':total, 'product_cost':subtotal_per_product, 'canceled_order':cancelled_order})

@login_required
def valid_user_order(request, order_id):
    order = get_object_or_404(Order, is_canceled=False, id=order_id)
    order_items = OrderItem.objects.filter(order=order)
    
    valid_order , created= ValidOrder.objects.get_or_create(original_order_object=order, user=order.user, shipping_info=order.shipping_address, total=order.total)
    valid_items = [ValidOrderItem.objects.create(validated_order=valid_order, product=x.product, quantity=x.quantity, price_at_validation=x.sutotal, sutotal=x.sutotal) for x in order_items]
    order.is_validated = True
    order.status = 'Completed'
    order.save()
    return HttpResponse(status=204)

@login_required
def valid_non_user_order(request, order_id):
    order = get_object_or_404(NonRegestredOrder, is_canceled=False, id=order_id)
    order_items = NonRegestredOrderItem.objects.filter(order=order)
    
    valid_order , created= ValidNonOrder.objects.get_or_create(original_order_object=order, user=order.user, shipping_info=order.shipping_address, total=order.total)
    valid_items = [ValidNonOrderItem.objects.create(validated_order=valid_order, product=x.product, quantity=x.quantity, price_at_validation=x.sutotal, sutotal=x.sutotal) for x in order_items]
    order.is_validated = True
    order.status = 'Completed'
    order.save()
    return HttpResponse(status=204)

@login_required
def show_valid_orders(request):
    orders = ValidOrder.objects.all()
    return render(request, 'order/valid_orders.html', {'orders':orders})

@login_required
def show_non_valid_orders(request):
    orders = ValidNonOrder.objects.all()
    return render(request, 'order/valid_orders.html', {'orders':orders, 'non_user':True})