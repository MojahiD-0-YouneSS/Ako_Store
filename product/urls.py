from django.urls import path
from . import views

app_name = 'product'

urlpatterns = [
    path('adding/', views.add_product, name='addProduct'),
    path('addColorSize/', views.add_color_size, name='addColorSize'),
    path('addFeaturesToProduct/', views.add_features_to_product, name='add_to_product'),
    path('detail/<int:pk>/', views.ProductDetail, name='detail'),
    path('delete/<int:id>/', views.Delete_product, name='delete'),
    path('brands/', views.brandlister, name='brandlister'),
    path('add_brand/', views.create_brand, name='add_brand'),
    path('add_product/', views.add_one_time_product, name='one_time_product'),
] 
