from django.db import models
from django.contrib.auth.models import User
from client.forms import ComeBackCode
from client.models import NonRegesteredClient
from product.models import  ProductModel, ProductColorSize
# Create your models here.

class Cart(models.Model):
    '''Cart: Represents a user's current shopping cart.'''
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(ProductModel, through='CartItem')
    total = models.IntegerField(default=0)
    def __str__(self):
        return f"Cart of {self.user.username}"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(ProductModel, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    color_size = models.ForeignKey(ProductColorSize, on_delete=models.CASCADE)
    is_ordered = models.BooleanField(default=False)
    def __str__(self):
        return f"{self.quantity} of {self.product.ProductName}"
    
    def save(self, *args, **kwargs):
        self.subtotal = float(self.product.ProductPrice) * self.quantity
        super().save(*args, **kwargs)

class TempraryCart(models.Model):
    '''Cart: Represents a user's current shopping cart.'''
    user = models.OneToOneField(NonRegesteredClient, on_delete=models.CASCADE)
    products = models.ManyToManyField(ProductModel, through='TempraryCartCartItem')
    total = models.IntegerField(default=0)
    def __str__(self):
        return f"Cart of {self.user.full_name}"

class TempraryCartCartItem(models.Model):
    cart = models.ForeignKey(TempraryCart, on_delete=models.CASCADE)
    product = models.ForeignKey(ProductModel, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    color_size = models.ForeignKey(ProductColorSize, on_delete=models.CASCADE, null=True)
    is_ordered = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.quantity} of {self.product.ProductName}"
    
    def save(self, *args, **kwargs):
        self.subtotal = float(self.product.ProductPrice) * self.quantity
        super().save(*args, **kwargs)

class WishList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ManyToManyField(ProductModel, through='WishListItem')

    def __str__(self):
        return f"{self.user.username}"

class WishListItem(models.Model):
    wish_list = models.ForeignKey(WishList, on_delete=models.CASCADE)
    product = models.ForeignKey(ProductModel, on_delete=models.CASCADE)
    added_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.wish_list.user.username} of {self.product.ProductName}"

