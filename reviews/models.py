from django.db import models
from django.contrib.auth.models import User
from product.models import ProductModel
from client.models import NonRegesteredClient

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    product = models.ForeignKey(ProductModel, on_delete=models.CASCADE, related_name='reviews')
    content = models.TextField()
    rating = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    replies_data = models.ManyToManyField('Reply',  related_name='replies')
    def __str__(self):
        return f'Review by {self.user.username} - {self.rating} stars'

class Reply(models.Model):
    review = models.ForeignKey(Review, on_delete=models.SET_NULL, null=True, blank=True, related_name='replies')
    reply_data = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    
    def __str__(self):
        return f'Review by {self.review.user.username} - {self.created_at}'
    

class BannedUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='banned_user')
    reason = models.TextField()
    banned_at = models.DateTimeField(auto_now_add=True)
    unbanned = models.BooleanField(default=False)
    def __str__(self):
        return f'Banned User: {self.user.username}'

class BannedNonUser(models.Model):
    user = models.OneToOneField(NonRegesteredClient, on_delete=models.CASCADE, related_name='banned_user')
    reason = models.TextField()
    banned_at = models.DateTimeField(auto_now_add=True)
    unbanned = models.BooleanField(default=False)
    def __str__(self):
        return f'Banned User: {self.user.username}'
