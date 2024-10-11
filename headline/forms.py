from django import forms
from .models import AdvertizmentHeadline


class AdvertizingForm(forms.ModelForm):
    
    class Meta:
        
        model =   AdvertizmentHeadline
        
        fields =     ['title' , 'description', 'image', 'is_active', 'for_product', 'product_number']
        
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }