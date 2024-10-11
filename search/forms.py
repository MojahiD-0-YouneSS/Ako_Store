from django import forms

# forms.py
class SearchForm(forms.Form):
    search_lables = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'class':'form-control'}),required=True)
    product_number = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class':'form-control'}),required=True)
