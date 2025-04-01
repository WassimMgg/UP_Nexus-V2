from django.db import models
from django.contrib.auth.models import User
from django.db.models import JSONField
# from PIL import Image

class Profile(models.Model):
    ROLE_CHOICES = [
        ('User', 'User'),
        ('Startup', 'Startup'),
        ('Freelancer', 'Freelancer'),
        ('Incubator', 'Incubator'),
        ('Accelerator', 'Accelerator'),
        ('Investor', 'Investor'),
        ('Project_holder', 'Project Holder'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES,default="User" ,  blank=True, null=True)
    pending_role = models.CharField(max_length=20, choices=ROLE_CHOICES, blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    city  = models.CharField(max_length=50, blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    facebook_link = models.URLField(blank=True, null=True)
    instagram_link = models.URLField(blank=True, null=True)
    linkedin_link = models.URLField(blank=True, null=True)
    services = models.CharField(max_length=100, blank=True, null=True)
    # Role-specific fields
    # Startup
    company_name = models.CharField(max_length=100, blank=True, null=True)
    business_license = models.FileField(upload_to='business_licenses/', blank=True, null=True)

    # Freelancer
    skills = models.CharField(max_length=200, blank=True, null=True)
    portfolio_link = models.URLField(blank=True, null=True)
    resume = models.FileField(upload_to='resumes/', blank=True, null=True)

    # Incubator
    incubator_name = models.CharField(max_length=100, blank=True, null=True)
    incubator_description = models.TextField(blank=True, null=True)
    incubator_certificate = models.FileField(upload_to='incubator_certificates/', blank=True, null=True)

    # Accelerator
    accelerator_name = models.CharField(max_length=100, blank=True, null=True)
    accelerator_description = models.TextField(blank=True, null=True)
    accelerator_certificate = models.FileField(upload_to='accelerator_certificates/', blank=True, null=True)

    # Investor
    investment_focus = models.CharField(max_length=200, blank=True, null=True)
    investment_stage = models.CharField(max_length=100, blank=True, null=True)
    investor_certificate = models.FileField(upload_to='investor_certificates/', blank=True, null=True)

    # Project Holder
    project_name = models.CharField(max_length=100, blank=True, null=True)
    project_description = models.TextField(blank=True, null=True)
    project_proposal = models.FileField(upload_to='project_proposals/', blank=True, null=True)

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)
class RoleRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=Profile.ROLE_CHOICES )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    role_specific_data = JSONField(default=dict)  # Store role-specific information (non-file data)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user.username} - {self.role} ({self.status})'