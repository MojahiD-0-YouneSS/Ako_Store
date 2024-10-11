from django import forms
from .models import PromotionModel, ShopPoster
class ProductFinderForm(forms.Form):
    ELEMENT_CHOICES = [
        ('all', 'ALL'),
        ('id', 'ID'),
        ('category parent', 'CATEGORY PARENT'),
        ('category child', 'CATEGORY CHILD'),
    ]
    input_data = forms.CharField(max_length=120,widget=forms.TextInput(attrs={'style':'width:500px', 'class':'mt-1 rounded'}))
    element = forms.ChoiceField(choices=ELEMENT_CHOICES, label='Select Product')
    
class DropdownForm(forms.Form):
    ELEMENT_CHOICES = [
        ('all', 'ALL'),
        ('id', 'ID'),
        ('category global', 'CATEGORY GLOBAL'),
        ('category privite', 'CATEGORY PRIVITE'),
        ('element4', 'Element 4'),
        ('element5', 'Element 5'),
        ('element6', 'Element 6'),
        ('element7', 'Element 7'),
        ('element8', 'Element 8'),
        ('element9', 'Element 9'),
    ]
    element = forms.ChoiceField(choices=ELEMENT_CHOICES, )
    
class PromotionForm(forms.ModelForm):
    class Meta:
        model = PromotionModel
        fields = ['rate', 'closed']

class FreezUnFreezPromotion(forms.Form):
    promotion_code = forms.CharField(max_length=15, widget=forms.TextInput(attrs={
        'class':"form-control mr-sm-2 mt-2 me-2 rounded",
        'id':"prsomo-code",
        'name':"promo-code",
        'type':"text",
        'placeholder':"Promotion Code:",
        'aria-label':"text" ,
        'style':"height:35px;"
    }))

class PosterForm(forms.ModelForm):
    class Meta:
        model = ShopPoster
        
        fields = ['title' , 'description', 'image', 'is_active', 'for_product', 'product_number', 'redirection_section']
        
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4, 'class': 'form-control description-class',},),
            'title': forms.TextInput(attrs={'class': 'form-control',},),
            'product_number': forms.TextInput(attrs={'class': 'form-control',},),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input',},),
            'for_product': forms.CheckboxInput(attrs={'class': 'form-check-input',},),
            'image': forms.FileInput(attrs={'class': 'form-control',},),
            'redirection_section':forms.Select(choices=[('A', 'a'), ('B', 'b'), ('C', 'c'), ('D', 'd')], attrs={'class': 'form-control'})
        }
        
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            for field_name, field in self.fields.items():
                if field_name == 'description':
                    field.widget.attrs.update({'class': 'form-control description-class', 'rows': 4})
                else:
                    field.widget.attrs.update({'class': 'form-control'})
