from django.urls import path
from . import views

app_name = 'filter'

urlpatterns = [
    path("home/", views.filter_options, name="filter_options"),
    path("products/", views.filter_output, name="products"),
    path("products/<str:brand>/", views.brand_filter, name="brand_filter"),
    path("products/category/<str:category>/", views.Category_filter, name="Category_filter"),
    path("products/material/<str:categoryC>/", views.Material_Fabric_filter, name="Material_Fabric_filter"),
]
