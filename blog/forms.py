from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'location', 'event_date', 'image']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter the title'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter the content'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter the location'}),
            'event_date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }