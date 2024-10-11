from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class PromotionModel(models.Model):
    code = models.CharField(max_length=20, unique=True)
    rate = models.DecimalField(max_digits=5, decimal_places=2)
    closed = models.BooleanField(default=False)
    def __str__(self):
        return self.code
    
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    promo_codes = models.ManyToManyField(PromotionModel, through='UserPromoCode')

    def __str__(self):
        return self.user.username

class UserPromoCode(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    promo_code = models.ForeignKey(PromotionModel, on_delete=models.CASCADE)
    used = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user_profile.user.username} - {self.promo_code.code}"    
class ShopPoster(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='poster_shop/', null=True,  blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    for_product  = models.BooleanField(default=False)
    product_number = models.CharField(max_length=50, null=True)
    redirection_section = models.CharField(max_length=50, null=True)
    def __str__(self):
        return self.title
