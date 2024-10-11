from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from client.models import NonRegesteredClient, Client
from cart.models import TempraryCart
from order.models import CancelledOrder, CancelledOrderItem, Order, CancelledNonOrder, CancelledNonOrderItem
from .models import ShoppingHistory, NonRegestredShoppingHistory
# Create your views here.
@login_required
def order_history(request):
    history = ShoppingHistory.objects.get(user=request.user)
    orders = history.orders.order_by('-created_at').exclude(is_canceled=True)
    return render(request, 'shoppingHistory/shopping_history.html', {'orders': orders})

def non_order_history(request):
    cart_id = request.session.get('cart_id')
    cart = TempraryCart.objects.get(id=cart_id)
    user = NonRegesteredClient.objects.get(full_name=cart.user.full_name, phone=cart.user.phone, address=cart.user.address, city=cart.user.city)
    try:
        non_history = NonRegestredShoppingHistory.objects.get(user=user)
        orders = non_history.orders.order_by('-created_at')
    except:
        non_history = None
        orders = None
    return render(request, 'shoppingHistory/non_shopping_history.html', {'orders': orders})

@login_required
def canceled_orders(request):
    cancelled_orders = CancelledOrder.objects.all()
    for co in cancelled_orders:
        cancelled_orders_items = CancelledOrderItem.objects.filter(cancelled_order=co)
        co.total = sum([ x.price_at_cancellation * x.quantity for x in cancelled_orders_items])     
        co.save()
    return render(request, 'shoppingHistory/canceled_order.html', {'orders': cancelled_orders})

@login_required
def non_canceled_orders(request):
    cancelled_orders = CancelledNonOrder.objects.all()
    for cancelled_order in cancelled_orders:
        
        cancelled_orders_items = CancelledNonOrderItem.objects.filter(cancelled_order=cancelled_order)
        cancelled_order.total = sum([ x.price_at_cancellation * x.quantity for x in cancelled_orders_items])     
        cancelled_order.save()
    return render(request, 'shoppingHistory/non_canceled_order.html', {'orders': cancelled_orders})

def shopping_history(request):
    history = ShoppingHistory.objects.all()
    return render(request, 'shoppingHistory/users_shopping.html', {'history':history})