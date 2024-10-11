from django import forms
from .models import Review, Reply

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['content', 'rating']
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Write your review...', 'rows':5}),
            'rating': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 5}),
        }

class ReplyForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields = ['reply_data']
        widgets = {
            'reply_data': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Write your reply...'}),
        }