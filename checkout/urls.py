from django.urls import path
from . import views
app_name = 'checkout'
urlpatterns = [
    path('checkout/', views.checkout, name='checkout'),
    path('non_regestred_checkout/', views.non_regestred_checkout, name='noncheckout'),
]