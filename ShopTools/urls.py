from django.urls import path
from . import views

app_name = 'shopTools'

urlpatterns = [
    path('total-sales-revenue/', views.total_sales_and_revenue_view, name='total_sales_and_revenue'),
    path('cancelled-orders/', views.cancelled_orders_view, name='cancelled_orders'),
    path('cart-abandonment/', views.cart_abandonment_view, name='cart_abandonment'),
    path('wishlist-activity/', views.wishlist_activity_view, name='wishlist_activity'),
    path('most-viewed-products/', views.most_viewed_products_view, name='most_viewed_products'),
    path('product-reviews/', views.product_reviews_view, name='product_reviews'),
    path('repeat-customers/', views.repeat_customers_view, name='repeat_customers'),
    path('promotion-effectiveness/', views.promotion_effectiveness_view, name='promotion_effectiveness'),
    path('headline-performance/', views.headline_performance_view, name='headline_performance'),
    path('customer-segmentation/', views.customer_segmentation_view, name='customer_segmentation'),
    path('conversion-rate/', views.conversion_rate_view, name='conversion_rate'),
    path('customer-lifetime-value/', views.customer_lifetime_value_view, name='customer_lifetime_value'),
    path('product-return-analysis/', views.product_return_analysis_view, name='product_return_analysis'),
    path('sentiment-analysis/', views.sentiment_analysis_view, name='sentiment_analysis'),
    path('geographical-sales/', views.geographical_sales_view, name='geographical_sales'),
    path('inventory-turnover/', views.inventory_turnover_view, name='inventory_turnover'),
]
