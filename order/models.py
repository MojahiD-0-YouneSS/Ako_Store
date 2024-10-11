from django.db import models
from django.contrib.auth.models import User
from client.models import NonRegesteredClient, Client
from product.models import ProductModel
# Create your models here.

class ShippingMethod(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    estimated_delivery_time = models.CharField(max_length=255)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class ShippingAddress(models.Model):
    user = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='shipping_addresses')
    full_name = models.CharField(max_length=255)
    address_line_1 = models.CharField(max_length=255)
    address_line_2 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255)
    state_or_region = models.CharField(max_length=255, blank=True, null=True)
    postal_code = models.CharField(max_length=20, blank=True, null=True)
    country = models.CharField(max_length=255, blank=True, null=True)
    phone_number = models.CharField(max_length=20)

class ShippingNonAddress(models.Model):
    user = models.ForeignKey(NonRegesteredClient, on_delete=models.CASCADE, related_name='shipping_addresses')
    full_name = models.CharField(max_length=255)
    address_line_1 = models.CharField(max_length=255)
    address_line_2 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255)
    state_or_region = models.CharField(max_length=255, blank=True, null=True)
    postal_code = models.CharField(max_length=20, blank=True, null=True)
    country = models.CharField(max_length=255, blank=True, null=True)
    phone_number = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.full_name}, {self.address_line_1}, {self.city}, {self.country}"

class Order(models.Model):
    '''Order: Represents an order made by a user.'''
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[('Pending', 'Pending'), ('Completed', 'Completed')])
    products = models.ManyToManyField(ProductModel, through='OrderItem')
    is_validated = models.BooleanField(default=False)
    is_canceled = models.BooleanField(default=False)
    total = models.IntegerField(default=0)
    shipping_method = models.ForeignKey(ShippingMethod, on_delete=models.SET_NULL, null=True)
    shipping_address = models.ForeignKey(ShippingAddress, on_delete=models.SET_NULL, null=True)
    shipping_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    
    def __str__(self):
        return f"Order {self.id} by {self.user.username}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(ProductModel, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    sutotal = models.IntegerField(default=0)
    
class NonRegestredOrder(models.Model):
    '''NonRegesteredOrder: Represents an order made by a user that don't have an acount.'''
    user = models.ForeignKey(NonRegesteredClient, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[('Pending', 'Pending'), ('Completed', 'Completed')])
    products = models.ManyToManyField(ProductModel, through='NonRegestredOrderItem')
    is_canceled = models.BooleanField(default=False)
    is_validated = models.BooleanField(default=False)
    total = models.IntegerField(default=0)
    shipping_method = models.ForeignKey(ShippingMethod, on_delete=models.SET_NULL, null=True)
    shipping_address = models.ForeignKey(ShippingNonAddress, on_delete=models.SET_NULL, null=True)
    shipping_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"Order {self.id} by {self.user.full_name}"

class NonRegestredOrderItem(models.Model):
    order = models.ForeignKey(NonRegestredOrder, on_delete=models.CASCADE)
    product = models.ForeignKey(ProductModel, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    sutotal = models.IntegerField(default=0)

class CancelledOrder(models.Model):
    original_order_object = models.ForeignKey(Order, on_delete=models.CASCADE, null=True)
    original_order_id = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)  # Optional, only for registered users
    cancelled_at = models.DateTimeField(auto_now_add=True)
    reason = models.TextField(null=True, blank=True)
    products = models.ManyToManyField(ProductModel, through='CancelledOrderItem')
    total = models.IntegerField(default=0)
    def __str__(self):
        return f"Cancelled Order {self.original_order_id} ({self.reason})"

class CancelledOrderItem(models.Model):
    cancelled_order = models.ForeignKey(CancelledOrder, on_delete=models.CASCADE)
    product = models.ForeignKey(ProductModel, on_delete=models.SET_NULL, null=True)
    quantity = models.PositiveIntegerField()
    price_at_cancellation = models.DecimalField(max_digits=10, decimal_places=2)
    sutotal = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.product.ProductName} - {self.quantity}"

class CancelledNonOrder(models.Model):
    original_order_object = models.ForeignKey(NonRegestredOrder, on_delete=models.CASCADE, null=True)
    original_order_id = models.IntegerField()
    user = models.ForeignKey(NonRegesteredClient, on_delete=models.SET_NULL, null=True, blank=True)  # Optional, only for registered users
    cancelled_at = models.DateTimeField(auto_now_add=True)
    reason = models.TextField(null=True, blank=True)
    products = models.ManyToManyField(ProductModel, through='CancelledNonOrderItem')
    total = models.IntegerField(default=0)
    def __str__(self):
        return f"Cancelled Order {self.original_order_id} ({self.reason})"

class CancelledNonOrderItem(models.Model):
    cancelled_order = models.ForeignKey(CancelledNonOrder, on_delete=models.CASCADE)
    product = models.ForeignKey(ProductModel, on_delete=models.SET_NULL, null=True)
    quantity = models.PositiveIntegerField()
    price_at_cancellation = models.DecimalField(max_digits=10, decimal_places=2)
    sutotal = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.product.ProductName} - {self.quantity}"

class ValidOrder(models.Model):
    original_order_object = models.ForeignKey(Order, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)  # Optional, only for registered users
    validated_at = models.DateTimeField(auto_now_add=True)
    shipping_info = models.TextField(null=True, blank=True)
    products = models.ManyToManyField(ProductModel, through='ValidOrderItem')
    total = models.IntegerField(default=0)
    def __str__(self):
        return f"Valid Order {self.original_order_object.id}"

class ValidOrderItem(models.Model):
    validated_order = models.ForeignKey(ValidOrder, on_delete=models.CASCADE)
    product = models.ForeignKey(ProductModel, on_delete=models.SET_NULL, null=True)
    quantity = models.PositiveIntegerField()
    price_at_validation = models.DecimalField(max_digits=10, decimal_places=2)
    sutotal = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.product.ProductName} - {self.quantity}"

class ValidNonOrder(models.Model):
    original_order_object = models.ForeignKey(NonRegestredOrder, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(NonRegesteredClient, on_delete=models.SET_NULL, null=True, blank=True)  # Optional, only for registered users
    validated_at = models.DateTimeField(auto_now_add=True)
    shipping_info = models.TextField(null=True, blank=True)
    products = models.ManyToManyField(ProductModel, through='ValidNonOrderItem')
    total = models.IntegerField(default=0)
    def __str__(self):
        return f"Valid Order {self.original_order_object.id}"

class ValidNonOrderItem(models.Model):
    validated_order = models.ForeignKey(ValidNonOrder, on_delete=models.CASCADE)
    product = models.ForeignKey(ProductModel, on_delete=models.SET_NULL, null=True)
    quantity = models.PositiveIntegerField()
    price_at_validation = models.DecimalField(max_digits=10, decimal_places=2)
    sutotal = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.product.ProductName} - {self.quantity}"
