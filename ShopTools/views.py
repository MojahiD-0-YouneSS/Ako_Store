from django.shortcuts import render
from django.db.models import Sum, F, Count, Avg, Q
from order.models import ValidOrderItem, CancelledOrderItem, ShippingAddress, Order, OrderItem
from cart.models import Cart, WishListItem
from shopingHistory.models import ShoppingHistory
from product.models import ProductModel
from reviews.models import Review
from client.models import Client
from Shop.models import UserPromoCode
from headline.models import HeadlinedProduct

def total_sales_and_revenue_view(request):
    total_sales = ValidOrderItem.objects.aggregate(total_sales=Sum(F('quantity') * F('price_at_validation')))['total_sales'] or 0
    revenue_by_product = ValidOrderItem.objects.values('product__ProductName').annotate(total_revenue=Sum(F('quantity') * F('price_at_validation')))
    
    data = {item['product__ProductName']: item['total_revenue'] for item in revenue_by_product}
    data['total_sales'] = total_sales
    context = {
        'title': 'Total Sales and Revenue',
        'data': data,
    }
    return render(request, 'shopTools/graph_view.html', context)

def cancelled_orders_view(request):
    cancelled_orders_count = CancelledOrderItem.objects.aggregate(total_cancelled=Count('id'))['total_cancelled']
    
    total_cancelled_value = CancelledOrderItem.objects.aggregate(total_value=Sum(F('quantity') * F('price_at_cancellation')))['total_value'] or 0

    context = {
        'title': 'Cancelled Orders',
        'data': {
            'Cancelled Orders Count': cancelled_orders_count,
            'Total Cancelled Value': total_cancelled_value,
        }
    }
    return render(request, 'shopTools/graph_view.html', context)

def cart_abandonment_view(request):
    abandoned_carts = Cart.objects.annotate(total_items=Count('cartitem'),unordered_items=Count('cartitem', filter=Q(cartitem__is_ordered=False))).filter(total_items=F('unordered_items')).count()

    context = {
        'title': 'Cart Abandonment',
        'data': {
            'Abandoned Carts': abandoned_carts,
        }
    }
    return render(request, 'shopTools/graph_view.html', context)

def wishlist_activity_view(request):
    wishlist_items_count = WishListItem.objects.aggregate(total_wishlist_items=Count('id'))['total_wishlist_items']

    context = {
        'title': 'Wishlist Activity',
        'data': {
            'Total Wishlist Items': wishlist_items_count,
        }
    }
    return render(request, 'shopTools/graph_view.html', context)

def most_viewed_products_view(request):
    most_viewed_products = ShoppingHistory.objects.values('orders__products__ProductName').annotate(view_count=Count('id')).order_by('-view_count')[:10]

    data = {item['orders__products__ProductName']: item['view_count'] for item in most_viewed_products}
    context = {
        'title': 'Most Viewed Products',
        'data': data,
    }
    return render(request, 'shopTools/graph_view.html', context)

def product_reviews_view(request):
    reviews_by_product = Review.objects.values('product__ProductName').annotate(review_count=Count('id'), average_rating=Avg('rating')).order_by('-review_count')

    data = {item['product__ProductName']: item['review_count'] for item in reviews_by_product}
    context = {
        'title': 'Product Reviews',
        'data': data,
    }
    return render(request, 'shopTools/graph_view.html', context)

def repeat_customers_view(request):
    repeat_customers = Order.objects.annotate(order_count=Count('user')).filter(order_count__gt=1).count()

    context = {
        'title': 'Repeat Customers',
        'data': {
            'Repeat Customers': repeat_customers,
        }
    }
    return render(request, 'shopTools/graph_view.html', context)

def promotion_effectiveness_view(request):
    promo_usage = UserPromoCode.objects.values('promo_code__code').annotate(usage_count=Count('id')).order_by('-usage_count')

    data = {item['promo_code__code']: item['usage_count'] for item in promo_usage}
    context = {
        'title': 'Promotion Effectiveness',
        'data': data,
    }
    return render(request, 'shopTools/graph_view.html', context)

def headline_performance_view(request):
    headline_performance = HeadlinedProduct.objects.values('product__ProductName').annotate(click_count=Count('id')).order_by('-click_count')

    data = {item['product__ProductName']: item['click_count'] for item in headline_performance}
    context = {
        'title': 'Headline Performance',
        'data': data,
    }
    return render(request, 'shopTools/graph_view.html', context)

def customer_segmentation_view(request):
    high_spenders = OrderItem.objects.annotate(total_spent=Sum(F('quantity') * F('product__ProductPrice'))).filter(total_spent__gte=500).count()
    frequent_shoppers = Order.objects.annotate(order_count=Count('user')).filter(order_count__gte=5).count()
    cart_abandoners = Cart.objects.filter(cartitem=Count('cartitem'),products=Count('cartitem', filter=Q(cartitem__is_ordered=False))).count()

    context = {
        'title': 'Customer Segmentation',
        'data': {
            'High Spenders': high_spenders,
            'Frequent Shoppers': frequent_shoppers,
            'Cart Abandoners': cart_abandoners,
        }
    }
    return render(request, 'shopTools/graph_view.html', context)

def conversion_rate_view(request):
    total_visits = ShoppingHistory.objects.count()
    total_orders = ValidOrderItem.objects.aggregate(total_orders=Sum('quantity'))['total_orders']
    conversion_rate = (total_orders / total_visits) * 100 if total_visits > 0 else 0

    context = {
        'title': 'Conversion Rate',
        'data': {
            'Total Visits': total_visits,
            'Total Orders': total_orders,
            'Conversion Rate (%)': conversion_rate,
        }
    }
    return render(request, 'shopTools/graph_view.html', context)

def customer_lifetime_value_view(request):
    average_order_value = Client.objects.aggregate(avg_order_value=Avg('order__total'))['avg_order_value']
    purchase_frequency = Client.objects.annotate(order_count=Count('order')).aggregate(avg_frequency=Avg('order_count'))['avg_frequency']
    customer_lifetime_value = average_order_value * purchase_frequency

    context = {
        'title': 'Customer Lifetime Value',
        'data': {
            'Average Order Value': average_order_value,
            'Purchase Frequency': purchase_frequency,
            'Customer Lifetime Value': customer_lifetime_value,
        }
    }
    return render(request, 'shopTools/graph_view.html', context)

def product_return_analysis_view(request):
    return_rate_by_product = CancelledOrderItem.objects.values('product__ProductName').annotate(return_count=Count('id')).order_by('-return_count')

    data = {item['product__ProductName']: item['return_count'] for item in return_rate_by_product}
    context = {
        'title': 'Product Return Analysis',
        'data': data,
    }
    return render(request, 'shopTools/graph_view.html', context)

def sentiment_analysis_view(request):
    positive_reviews = Review.objects.filter(rating__gte=4).count()
    neutral_reviews = Review.objects.filter(rating=3).count()
    negative_reviews = Review.objects.filter(rating__lte=2).count()

    context = {
        'title': 'Sentiment Analysis',
        'data': {
            'Positive Reviews': positive_reviews,
            'Neutral Reviews': neutral_reviews,
            'Negative Reviews': negative_reviews,
        }
    }
    return render(request, 'shopTools/graph_view.html', context)

def geographical_sales_view(request):
    sales_by_region = ShippingAddress.objects.values('country')

    data = {item['country']: item['total_sales'] for item in sales_by_region}
    context = {
        'title': 'Geographical Sales',
        'data': data,
    }
    return render(request, 'shopTools/graph_view.html', context)

def inventory_turnover_view(request):
    empty_stock_products = ProductModel.objects.filter(in_stock__lte=False).order_by('in_stock')
    low_stock_products = ProductModel.objects.filter(quantity__lte=10).order_by('ProductName')
    high_turnover_products = ProductModel.objects.annotate(turnover_rate=Count('orderitem')).order_by('-turnover_rate')

    data = {
        'Low Stock Products': low_stock_products.count(),
        'High Turnover Products': high_turnover_products.count(),
        'Empty Stock Products': empty_stock_products.count(),
    }
    context = {
        'title': 'Inventory Turnover',
        'data': data,
    }
    return render(request, 'shopTools/graph_view.html', context)
