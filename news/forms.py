from django import forms
from .models import Article , NewsletterSubscriber

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'summary', 'content', 'category', 'image']  # Added image
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            
            'summary': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 3}),
            'content': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 5}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-input-file'}),
        }
        
    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image:
            if image.size > 5*1024*1024:
                raise forms.ValidationError("Image file too large ( > 5MB )")
            if not image.name.lower().endswith(('.png', '.jpg', '.jpeg')):
                raise forms.ValidationError("Only PNG, JPG, and JPEG formats allowed")
        return image
class NewsletterSubscriptionForm(forms.ModelForm):
    class Meta:
        model = NewsletterSubscriber
        fields = ['email']
        widgets = {
            'email': forms.EmailInput(attrs={
                'class': 'w-full px-4 py-3 rounded-lg border border-gray-700 bg-gray-800 text-white focus:outline-none focus:ring-2 focus:ring-[#ffd502] focus:border-transparent',
                'placeholder': 'Your email address'
            })
        }
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if NewsletterSubscriber.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already subscribed.")
        return email