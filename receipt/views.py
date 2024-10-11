from django.shortcuts import render, get_object_or_404, redirect
from .models import Receipt, ReceiptItems
from order.models import ValidOrder, ValidNonOrderItem, ValidNonOrder, ValidOrderItem
from datetime import timedelta
from django.http import HttpResponse
# Create your views here.

def ClientReceipt(request):
    receiptinfo = Receipt.objects.all()
    
    return render(request, 'receipts/clientReceipt.html', {
        'receipts':receiptinfo
    })


def StoreReceipt(request):
    receiptinfo = Receipt.objects.all()
    return render(request, 'receipts/shopReceipt.html', {
        'receipts':receiptinfo
    })

def reciept_pdf(request, receipt_id):
    receipt = get_object_or_404(Receipt, receipt_reference=receipt_id)
    pdf = receipt.generate_pdf()
    return redirect('/')

def generate_receipt(request):
    valid_orders = ValidOrder.objects.all()
    for order in valid_orders:
        reciept, created = Receipt.objects.get_or_create(receipt_order=order)
        if created:
           reciept.expiredateValue = reciept.creationDate + timedelta(days=10)
           reciept.save()
           
           items = ValidOrderItem.objects.filter(validated_order=order)
           for item in items:
               ReceiptItems.objects.get_or_create(
                   receipt=reciept,
                   product=item,
                   quantity=item.quantity,
                   tax=0.0,
               )
        
    return HttpResponse(status=204)