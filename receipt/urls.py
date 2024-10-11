from django.urls import path
from . import views
app_name = 'receipt'
urlpatterns = [
    path('ClientReciepts/', views.ClientReceipt, name='clientReceipt'),
    path('StoreReciepts/', views.StoreReceipt,name='adminReceipt'),
    path('generate_Reciepts/', views.generate_receipt,name='generate_receipt'),
    path('RecieptsPdf/<int:receipt_id>/', views.reciept_pdf,name='reciept_pdf'),
]
