from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from PIL import Image

class Post(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    title = models.CharField(max_length=50)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    location = models.CharField(max_length=50, default="Unknown")
    event_date = models.DateTimeField(default=timezone.now)
    event_end_date = models.DateTimeField(default=timezone.now)
    image = models.ImageField(upload_to='images/', default='default.jpg', blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    requester = models.ForeignKey(User, on_delete=models.CASCADE, related_name='requested_posts' , default=None, blank=True, null=True)  

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})


class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    parent = models.ForeignKey('self', null=True, blank=True, related_name='replies', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(null=True, blank=True, help_text="When this comment was last edited")


    def mark_edited(self):
        self.edited_at = timezone.now()
        self.save(update_fields=['edited_at'])

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.content[:20]}"

    def is_reply(self):
        return self.parent is not None
   

    

