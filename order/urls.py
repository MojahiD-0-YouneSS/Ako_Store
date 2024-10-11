from django.urls import path
from . import views
from shopingHistory.views import order_history, non_order_history, canceled_orders, non_canceled_orders, shopping_history
app_name ='order'

urlpatterns = [
    path('pending/', views.pending_orders_view, name='pending'),
    path('all/', views.list_all_orders, name='list_all'),
    path('detail/<int:order_id>/', views.order_detail_view, name='order_detail'),
    path('non_detail/<int:order_id>/', views.non_order_detail_view, name='non_order_detail'),
    path('shop/non_order_detail/<int:order_id>/', views.shop_non_order_detail_view, name='shop_non_order_detail'),
    path('shop/order_detail/<int:order_id>/', views.shop_order_detail_view, name='shop_order_detail'),
    path('cancelled/order_detail/<int:order_id>/', views.canceled_order_detail_view, name='canceled_order_detail'),
    path('ready_to_ship/<int:order_id>/<str:user_email>/', views.update_order_status_view, name='valid'),
    path('user_orders/<int:user_id>/', views.user_orders_view, name='user_orders'),
    path('orders/', order_history, name='order_history'),
    path('non_orders/', non_order_history, name='non_order_history'),
    path('cancelled_orders/', canceled_orders, name='canceled_orders'),
    path('cancelled_non_orders/', non_canceled_orders, name='non_canceled_orders'),
    path('shop/order/<int:order_id>/', views.non_order_detail_view, name='non_order_detail_view'),
    path('shop/canceled/order/<int:order_id>/', views.canceled_order_detail_view, name='canceled_order_detail_view'),
    path('shop/canceled/non_order/<int:order_id>/', views.non_canceled_order_detail, name='canceled_non_order_detail_view'),
    path('shop/orders/', views.nonlist_all, name='nonlist_all'),
    path('shop/orders/<int:order_id>/cancelled', views.cancel_order, name='cancel_order'),
    path('shop/non_orders/<int:order_id>/cancelled', views.cancel_non_order, name='cancel_non_order'),    
    path('shop/order/<int:order_id>/update/', views.update_order_status_view, name='update_order_status'),
    path('shop/order/history/all/', shopping_history, name='shopping_history_all'),
    path('shop/order/<int:order_id>/update_to/valid/', views.valid_user_order, name='valid_order'),
    path('shop/non_order/<int:order_id>/update_to/valid/', views.valid_non_user_order, name='valid_non_order'),
    path('shop/order/valid/all/', views.show_non_valid_orders, name='show_non_valid_orders'),
    path('shop/non_order/valid/all/', views.show_valid_orders, name='show_valid_orders'),
]
