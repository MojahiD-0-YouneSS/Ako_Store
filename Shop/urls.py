from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'shop'
urlpatterns = [
    path('Interface/', views.shopInterface, name='shopInterface'),
    path('product/', views.ProductDetailView.as_view(), name='product_detail'),
    path('dropdown/', views.process_selected_element, name='dropdown'),
    path('delete/', views.delete_all_products, name='delete_all'),
    path('promotion/', views.PromotionCode, name='promotion'),
    path('get_promo_code/', views.get_promo_code, name='get_promo_code'),
    path('freez_promo_code/<str:promo_code>/', views.freezUnfreezCode, name='freez_promo_code'),
    path('regestred/', views.regestred_users, name='regestred_clients'),
    path('banned/users/', views.banned_users, name='banned_user'),
    path('nonregestred/', views.users_without_acounts, name='non_users'),
    path('banned/non_users/', views.banned_users_without_acounts, name='banned_non_user'),
    path('regestred_info/<str:username>/', views.userinfo, name='regestred_clients_infos'),
    path('non_regestred_info/<int:user_id>/', views.nonuserinfo, name='non_regestred_clients_infos'),
    path('gallery/', views.product_view, name='gallery'),
    path('poster/', views.poster_setter, name='poster'),
    path('poster/uploader/', views.poster_uploader, name='poster_uploader'),
    path('product/fabric/', views.fabric_adder, name='fabric_adder'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]