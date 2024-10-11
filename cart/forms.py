from django import forms
from .models import CartItem
class CartQuantityForm(forms.ModelForm):
    class Meta:
        model = CartItem
        fields = ['quantity']

class AplyPromotion(forms.Form):
    promo_code = forms.CharField(max_length=15, widget=forms.TextInput(attrs={
        'class':"form-control mr-sm-2 mt-2 me-2 rounded",
        'id':"prsomo-code",
        'name':"promo-code",
        'type':"text",
        'placeholder':"Promotion Code:",
        'aria-label':"text" ,
        'style':"height:35px;"
    }))
    
    
    