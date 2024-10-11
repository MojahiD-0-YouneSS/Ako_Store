from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from random import random, randint
from product.models import ProductModel
from order.models import ValidOrder, ValidOrderItem, ValidNonOrder, ValidNonOrderItem
# Create your models here.
from django.core.files.base import ContentFile

from django.utils import timezone
from datetime import timedelta
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from io import BytesIO

def id_sequence():
    id = [f'{randint(0, 10000)}' for _ in range(10)]
    return ''.join(id)[0:11]

def generate_random_sequence():
    id = id_sequence()
    ids = [receipt.id for receipt in Receipt.objects.all()]
    while id in ids:
        id = id_sequence()
    return id

class Receipt(models.Model):
    STATUS_CHOICES = [
        ('issued', 'Issued'),
        ('sent', 'Sent'),
        ('expired', 'Expired'),
    ]

    expiredateValue = models.CharField(max_length=30, default='')
    receipt_reference = models.CharField(max_length=10, default=generate_random_sequence, primary_key=True)
    creationDate = models.DateTimeField(auto_now_add=True, null=True)
    receipt_order = models.ForeignKey(ValidOrder, on_delete=models.CASCADE, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='issued')
    pdf_file = models.FileField(upload_to='receipt_pdf/', null=True, blank=True)

    class Meta:
        verbose_name = _("Receipt")
        verbose_name_plural = _("Receipts")

    def __str__(self):
        return f"Receipt {self.receipt_reference}"

    def calculate_total(self):
        
        total = sum(float(item.ProductPrice) * (1 + 0.0 / 100) * item.quantity for item in self.receipt_order.products.all())
        return total

    def is_expired(self):
        expiration_date = self.creationDate + timedelta(days=self.expiredateValue)
        return timezone.now() > expiration_date

    def generate_pdf(self):
        buffer = BytesIO()
        pdf = canvas.Canvas(buffer, pagesize=letter)
        width, height = letter

        pdf.drawString(1 * inch, height - 1 * inch, f"Receipt Reference: {self.receipt_reference}")
        pdf.drawString(1 * inch, height - 1.5 * inch, f"Creation Date: {self.creationDate.strftime('%Y-%m-%d')}")
        pdf.drawString(1 * inch, height - 2 * inch, f"Total Amount: {self.calculate_total()}")

        pdf.drawString(1 * inch, height - 3 * inch, "Items:")

        y = height - 3.5 * inch
        for item in self.receipt_order.products.all():
            pdf.drawString(1 * inch, y, f"Product: {item.ProductName} - Quantity: {item.quantity} - Price: {item.ProductPrice}")
            y -= 0.5 * inch

        pdf.showPage()
        pdf.save()

        buffer.seek(0)
        file_name = f"receipt_{self.receipt_reference}.pdf"
        self.pdf_file.save(file_name, ContentFile(buffer.getvalue()), save=False)
        return buffer
    def email_receipt(self, email_address):
        pdf = self.generate_pdf()
        email = EmailMessage(
            'Your Receipt',
            'Please find your receipt attached.',
            'from@example.com',
            [email_address],
        )
        email.attach('receipt.pdf', pdf, 'application/pdf')
        email.send()

class ReceiptItems(models.Model):
    receipt = models.ForeignKey(Receipt, on_delete=models.CASCADE)
    product = models.ForeignKey(ValidOrderItem, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    tax = models.DecimalField(max_digits=5, decimal_places=2, default=1.00)

    class Meta:
        verbose_name = _("Receipt Item")
        verbose_name_plural = _("Receipt Items")

    def __str__(self):
        return f"Receipt Item {self.id}"

class ShopReceipt(models.Model):
    expiredateValue = models.ManyToManyField(Receipt)
    downlowdedReceipts = models.IntegerField(default=0)
    expireedReceipts = models.IntegerField(default=0)
    id = models.CharField(max_length=10, default=generate_random_sequence, primary_key=True)
    class Meta:
        verbose_name = _("Shop Receipt")
        verbose_name_plural = _("Shop Receipts")

    def __str__(self):
        return f"Receipt {self.id}"
