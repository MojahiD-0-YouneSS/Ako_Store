from django.db import models
from product.models import ProductModel
# Create your models here.

class HeadlinedProduct(models.Model):
    product = models.OneToOneField(ProductModel, on_delete=models.CASCADE, related_name='headline_product')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.product.ProductName
    
class AdvertizmentHeadline(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='advertizement_shop/', null=True,  blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    for_product  = models.BooleanField(default=False)
    product_number = models.CharField(max_length=50, null=True)
    def __str__(self):
        return self.title
