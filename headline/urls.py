from django.urls import path
from . import views
app_name = 'headline'

urlpatterns = [
    path('hedline/', views.ProductHeadline, name='hedline'),
    path('advertizment/', views.Advertaisment, name='advertizment'),
    path('adshow/', views.clientAds, name='adshow'),
    path('Topliner/', views.TopWearHeadline, name='Topliner'),
    path('ads_list/', views.ads_list, name='ads_list'),
    path('outfit_selector/<str:topwareref>/<str:legwareref>/<str:feetwareref>/<str:usr>/', views.outfit_selector, name='outfit_selector'),
    path('delete-ad/<int:ad_id>/', views.Delete_Advertisment, name='delete_ad'),
    path('tags/', views.ProductTagsHeadline, name='tagheadline')
]