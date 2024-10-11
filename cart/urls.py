from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('', views.view_cart, name='view_cart'),
    path('summary/', views.cart_summary, name='summary'),
    path('add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('update/<int:product_id>/<int:color_id>/', views.update_cart, name='update_cart'),
    path('create_temp_cart/<str:known_client>/', views.create_temp_cart, name='create_temp_cart'),
    path('add_to_temp_cart/<int:product_id>/', views.add_to_temp_cart, name='add_to_temp_cart'),
    path('view_temp_cart/', views.view_temp_cart, name='view_temp_cart'),
    path('remove_from_temp_cart/<int:product_id>/', views.remove_from_temp_cart, name='remove_from_temp_cart'),
    path('finalize_order/', views.finalize_order, name='finalize_order'),
    path('finalize_non_order/', views.finalize_non_order, name='finalize_non_order'),
    path('options/', views.unknown_client_options, name='unknown_client_options'),
    path('wishlist/', views.view_wish_list, name='view_wish_list'),
    path('wishlist/add/<int:product_id>/', views.add_wish_list, name='add_wish_list'),
    path('wishlist/remove/<int:product_id>/', views.remove_wish_list, name='remove_wish_list'),
    path('wishlist/summary/', views.wish_list_summary, name='wish_list_summary'),
    
]