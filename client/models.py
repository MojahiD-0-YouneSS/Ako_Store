from django.db import models
from django.urls import reverse
from django.utils.translation import gettext as _
from django.contrib.auth.models import User

# Create your models here.

class Client_User_Tag(models.Model):
    user =  models.OneToOneField(User, on_delete=models.CASCADE)
    client =  models.OneToOneField('Client', on_delete=models.CASCADE)

class Client(models.Model):
    full_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.EmailField(max_length=50)
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    class Meta:
        verbose_name = _("Client")
        verbose_name_plural = _("Clients")

    def __str__(self):
        return self.full_name

    def get_absolute_url(self):
        return reverse("Client_detail", kwargs={"pk": self.pk}) 

class NonRegesteredClient(models.Model):
    full_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=200)
    email = models.EmailField(max_length=50, null=True, blank=True)
    city = models.CharField(max_length=100)
    comeback_code = models.CharField(max_length=20, unique=True, null=True, blank=True)  
    is_active = models.BooleanField(default=True)    
    class Meta:
        verbose_name = _("NonRegesteredClient")
        verbose_name_plural = _("NonRegesteredClients")

    def __str__(self):
        return self.full_name

    def get_absolute_url(self):
        return reverse("Client_detail", kwargs={"pk": self.pk}) 

'''
class shoppingBehavior(models.model):
    pass

class PersonnalPreferences(models.model):
    pass
    
class Engagement_and_Loyalty
'''