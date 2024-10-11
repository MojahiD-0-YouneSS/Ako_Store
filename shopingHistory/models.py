from django.db import models
from django.contrib.auth.models import User
from client.models import NonRegesteredClient
from order.models import Order, NonRegestredOrder
# Create your models here.
class ShoppingHistory(models.Model):
    """ShoppingHistory: Represents the historical record of all the orders made by a user."""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    orders = models.ManyToManyField(Order)

    def __str__(self):
        return f"ShoppingHistory of {self.user.username}"

class NonRegestredShoppingHistory(models.Model):
    """ShoppingHistory: Represents the historical record of all the orders made by a user."""
    user = models.ForeignKey(NonRegesteredClient, on_delete=models.CASCADE)
    orders = models.ManyToManyField(NonRegestredOrder)

    def __str__(self):
        return f"ShoppingHistory of {self.user.full_name}"