from django.urls import path
from . import views

app_name = 'client'

urlpatterns = [
    path('informations/', views.Client_data_hundler, name='informations'),
    path('Profile/<int:user_id>/', views.Client_Profile, name='profile'),
    path('nonRegestredinformations/', views.Non_Regestred_Client_data_hundler, name='nonRegestredinformations'),
    path('ban_user/<str:user_name>/', views.ban_client, name='ban_client'),
    path('ban/non_user/<int:user_id>/', views.ban_non_client, name='ban_non_client'),
    path('unban/non_user/<int:user_id>/', views.unban_non_user, name='unban_non_client'),
    path('unban_user/<str:user_name>/', views.unban_user, name='unban_client'),
]
