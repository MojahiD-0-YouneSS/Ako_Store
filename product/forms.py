from django import forms
from .models import ProductFabric, ProductModel, ProductColor, ProductSize, ProductCategoryParent, ProductCategoryChild, Tags, ProductImage, SIZE, Color, BrandModel, ProductBrand
from django.core.exceptions import ValidationError
import re

class ProductModelForm(forms.ModelForm):
    class Meta:
        model = ProductModel
        fields = ['ProductName', 
                  'ProductPrice',
                  'in_stock',
                  'ProductSKU', 
                  'ProductDescription',
                  'available_from', 
                  'available_until',
                  'quantity',
                  'headding',
                  'returned',
                  'original',
                  'gifted',]
        lables = {
            'ProductName': 'Product Name',
            'ProductPrice': 'Product Price',
            'in_stock': 'In Stock',
            'ProductSKU': 'Product SKU',
            'ProductDescription': 'Product Description',
            'available_from': 'Available From',
            'available_until': 'Available Until',
            'quantity': 'Quantity',
            'headding': 'Headding',
            'returned': 'Returned',
            'original': 'Original',
            'gifted': 'Gifted',
        }
        
        widget = {
            'reviews': forms.CheckboxSelectMultiple(attrs={'class': 'form-control',}),
            'related_products': forms.CheckboxSelectMultiple(attrs={'class': 'form-control',}),
            'ProductDescription': forms.Textarea(attrs={'rows': 4, 'cols': 40, 'class': 'form-control',})
        }

class ProductImageForm(forms.ModelForm):
    Product_Image = forms.FileField(required=False, widget = forms.TextInput(attrs={
            "name": "images",
            "type": "File",
            "class": "form-control",
            "multiple": "True",
        }), label = "")
    class Meta: 
        model = ProductImage
        fields = ['Product_Image']        

class Color_Size_Adder_Form(forms.Form):
    SWITCH_ELEMENTS = [('color', 'Color'),
        ('size', 'Size')]
    switcher = forms.ChoiceField(choices=SWITCH_ELEMENTS)
    chain = forms.CharField(
        max_length=255,
        help_text="<strong>Enter names separated by ','. Use spaces for two-word names.</strong>",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter color or size names separated by commas'
        }),
    )
    action = forms.CharField(widget=forms.HiddenInput(), initial='add')
    def clean_chain(self):
        chain = self.cleaned_data.get('chain')
        switcher = self.cleaned_data.get('switcher')

        if switcher == 'color':
            if not all(char.isalpha() or char.isspace() or char == ',' for char in chain):
                raise ValidationError('Color names can only contain alphabetic characters, spaces, and commas.')
        elif switcher == 'size':
            if not all(char.isalnum() or char.isspace() or char == ',' for char in chain):
                raise ValidationError('Size names can contain alphanumeric characters, spaces, and commas.')

        return chain
    
class ProductCategoryPForm(forms.Form):
    category = forms.ModelChoiceField(queryset=ProductCategoryParent.objects.all(), empty_label="Select a Category")
        
class ProductCategoryCForm(forms.ModelForm):
    class Meta:
        model = ProductCategoryChild
        fields = ['ProductCategoryC',]
        labels = {
            'ProductCategoryC': 'Sub-Category',
        }
                
class ProductTagsForm(forms.ModelForm):
    class Meta:
        model = Tags
        fields = ['New', 'Limited', 'Ondemand', 'Viral']
        labels = {
            'New': 'New-',
            'Limited': 'Limited',
            'Ondemand': 'On Demand',
            'Viral': 'Viral'
        }

class ProductColorForm(forms.ModelForm):
    class Meta:
        model = ProductColor
        fields = ['color','quantity']
        widgets = {
            'quantity': forms.NumberInput(attrs={'id': 'id_quantity_color'})
        }

class ProductSizeForm(forms.ModelForm):
    class Meta:
        model = ProductSize
        fields = ['size', 'quantity']
        widgets = {
            'quantity': forms.NumberInput(attrs={'id': 'id_quantity_size'})
        }

class That_One_Product_Form(forms.Form):
    reference_ID = forms.CharField(max_length=20, help_text="<strong>Enter Product Reference Example : 1a2b55wfwwf4w84f4w84.</strong>",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter color or size names separated by commas'
        }),
    )
    def process_color_and_size_forms(self,color_form, size_form):
        if self.is_valid():
            reference_number = self.cleaned_data.get('reference_ID')
            try:
                product = ProductModel.objects.get(reference_number=reference_number)
                is_valid = True
            except ProductModel.DoesNotExist:
                is_valid = False
                product = None
        else:
            is_valid = False
            product = None

        return is_valid, product, (color_form, size_form)
INPUT_CLASSES = 'col-12 py-4 rounded-xl border'

class EditProductForm(forms.ModelForm):
    class Meta:
        model = ProductModel
        fields = ['ProductName',  'in_stock', 'ProductSKU', 
                  'related_products', 'available_from', 
                  'available_until', 'quantity', 'headding', 'returned',
                ]
        lables = {
            'ProductName': 'Product Name',
            'ProductPrice': 'Product Price',
            'in_stock': 'In Stock',
            'ProductSKU': 'Product SKU',
            'ProductCategoriesParent': 'Parent Categories',
            'ProductCategoriesChild': 'Child Categories',
            'customization_options': 'Customization Options',
            'size': 'Size',
            'available_from': 'Available From',
            'available_until': 'Available Until',
            'quantity': 'Quantity',
            'headding': 'Headding',
            'returned': 'Returned',
            'original': 'Original',
            'gifted': 'Gifted',
        }
        
        widget = {
            'ProductCategoriesParent': forms.CheckboxSelectMultiple,
            'ProductCategoriesChild': forms.CheckboxSelectMultiple,
            'reviews': forms.CheckboxSelectMultiple,
            'related_products': forms.CheckboxSelectMultiple,
            'tags': forms.CheckboxSelectMultiple,
            'customization_options': forms.Textarea(attrs={'rows': 4, 'cols': 40})
        }

class BrandForm(forms.ModelForm):
    ref_number = forms.CharField(required=False,max_length=55,widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter reffrence number for a product'
        }),)
    class Meta:
        model = BrandModel
        fields = ['name', 'brand_Image']
        widgets={
        'name':forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter brand name',
        }),
        'brand_Image':forms.FileInput(attrs={
            'class': 'form-control',
            'placeholder': 'Upload Brand Image',
        }),
        }
        
    def clean_name(self):
        name = self.cleaned_data.get('name')
        if BrandModel.objects.filter(name=name).exists():
            existing_brand = BrandModel.objects.get(name=name)
            # If the brand exists, don't raise the default error
            return name
        return name
    
    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get('name')
        brand_Image = cleaned_data.get('brand_Image')
        if BrandModel.objects.filter(name=name).exists():
            existing_brand = BrandModel.objects.get(name=name)
            if not brand_Image:
                # If no new image is provided, don't raise an error but use the existing brand's image
                cleaned_data['brand_Image'] = existing_brand.brand_Image
        else:
            if not brand_Image:
                self.add_error('brand_Image', 'An image is required for a new brand.')
                
        return cleaned_data

class ProductFabricForm(forms.Form):
    pure = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        label='Is Pure Fabric?'
    )
    fabric = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Example: cotton or 15% cotton, 75% nylon'
        }),
        label='Fabric Composition'
    )
    product = forms.CharField(required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label='Product Reference Number'
    )
    