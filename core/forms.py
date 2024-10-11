from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

Class = 'col-12 py-4 rounded w-1/2 text-center'

class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder':'Your username',
        'class':Class,
    }))
    
    email = forms.CharField(widget=forms.EmailInput(attrs={
        'placeholder':'Your email address',
        'class':Class,
    }))
    
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder':'Your password',
        'class':Class,
    }))
    
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder':'repeat password',
        'class':Class,
    }))
    
class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder':'Your username',
        'class':Class,
    }))
    
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder':'Your password',
        'class':Class,
    }))
    