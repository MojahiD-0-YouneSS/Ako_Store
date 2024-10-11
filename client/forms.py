# forms.py
from django import forms
from .models import Client, NonRegesteredClient

Class = 'shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline'
LABEL_CLASSES = 'block text-gray-700 text-sm font-bold mb-2'

class ClientForm(forms.ModelForm):
    new_email = forms.EmailField(required=False, widget=forms.EmailInput(attrs={
        'placeholder': 'New email (optional)',
    }))
    class Meta:
        model = Client
        fields = ('full_name', 'phone', 'address', 'city')
        labels = {
            'phone': 'phone Number',
            'full_name': 'Full Name',
            'address': 'address',
            'city': 'city',
        }
        widget = {
            'full_name': forms.TextInput(attrs={
            'placeholder': labels['full_name'],
        }),
            'phone': forms.TextInput(attrs={
            'placeholder': labels['phone'],
        }),
            'address': forms.TextInput(attrs={
            'placeholder': labels['address'],
        })
            ,'city': forms.TextInput(attrs={
            'placeholder': labels['city'],
        }),
        }
        
    def save(self, commit=True):
        instance = super().save(commit=False)
        new_email = self.cleaned_data.get('new_email')
        if new_email:
            instance.email = new_email
        else:
            # Use email field name of the User model as default if not provided
            instance.email = instance.email
        if commit:
            instance.save()
        return instance

class ComeBackCode(forms.Form):
    comeback_code = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'placeholder': 'Come-back Code', 'class':'form-control'}), help_text='<strong>Create a unique come-back code (e.g., your Rabat2025)</strong>',)


class NonRegesteredClientForm(forms.ModelForm):
    """Form definition for NonRegesteredClient."""
    class Meta:
        """Meta definition for NonRegesteredClientform."""
        model = NonRegesteredClient
        fields = ('full_name', 'phone', 'address', 'city',)
        labels = {
            'phone': 'phone Number',
            'full_name': 'Full Name',
            'address': 'address',
            'city': 'city',
        }
        widget = {
            'full_name': forms.TextInput(attrs={
            'placeholder': labels['full_name'],
        }),
            'phone': forms.TextInput(attrs={
            'placeholder': labels['phone'],
        }),
            'address': forms.TextInput(attrs={
            'placeholder': labels['address'],
        })
            ,'city': forms.TextInput(attrs={
            'placeholder': labels['city'],
        }),
        }
        help_texts = {
            'full_name': 'You will not receive monthly promotion codes if you don\'t sign up.',
        }