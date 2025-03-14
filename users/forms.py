from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile

class UserRegisterForm(UserCreationForm):
    # email = forms.EmailField()
    phone_number = forms.CharField(max_length=15)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'phone_number' ]

    def save(self, commit=True):
        user = super().save(commit=False)
    # Create profile without 'commit' argument
        profile = Profile(user=user, phone_number=self.cleaned_data['phone_number'])
    
        if commit:
            user.save()  
            profile.save() 
        
        return user  # Typically return the user object
    
class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']



class StartupVerificationForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['company_name', 'business_license']

class FreelancerVerificationForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['skills', 'portfolio_link', 'resume']

class IncubatorVerificationForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['incubator_name', 'incubator_description', 'incubator_certificate']

class AcceleratorVerificationForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['accelerator_name', 'accelerator_description', 'accelerator_certificate']

class InvestorVerificationForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['investment_focus', 'investment_stage', 'investor_certificate']

class ProjectHolderVerificationForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['project_name', 'project_description', 'project_proposal']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image', 'phone_number']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        profile = self.instance

        # Dynamically add fields based on the approved role
        if profile.role == 'startup':
            self.fields['company_name'] = forms.CharField(max_length=100, required=False)
            self.fields['business_license'] = forms.FileField(required=False)
        elif profile.role == 'freelancer':
            self.fields['skills'] = forms.CharField(max_length=200, required=False)
            self.fields['portfolio_link'] = forms.URLField(required=False)
            self.fields['resume'] = forms.FileField(required=False)
        elif profile.role == 'incubator':
            self.fields['incubator_name'] = forms.CharField(max_length=100, required=False)
            self.fields['incubator_description'] = forms.CharField(widget=forms.Textarea, required=False)
            self.fields['incubator_certificate'] = forms.FileField(required=False)
        elif profile.role == 'accelerator':
            self.fields['accelerator_name'] = forms.CharField(max_length=100, required=False)
            self.fields['accelerator_description'] = forms.CharField(widget=forms.Textarea, required=False)
            self.fields['accelerator_certificate'] = forms.FileField(required=False)
        elif profile.role == 'investor':
            self.fields['investment_focus'] = forms.CharField(max_length=200, required=False)
            self.fields['investment_stage'] = forms.CharField(max_length=100, required=False)
            self.fields['investor_certificate'] = forms.FileField(required=False)
        elif profile.role == 'project_holder':
            self.fields['project_name'] = forms.CharField(max_length=100, required=False)
            self.fields['project_description'] = forms.CharField(widget=forms.Textarea, required=False)
            self.fields['project_proposal'] = forms.FileField(required=False)

class RoleSelectionForm(forms.Form):
    role = forms.ChoiceField(choices=Profile.ROLE_CHOICES, required=True)