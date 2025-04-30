from django.contrib import admin
from .models import Article , NewsletterSubscriber

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'published_date')
    list_filter = ('category',)
    search_fields = ('title', 'summary', 'author', 'category')

@admin.register(NewsletterSubscriber)
class NewsletterSubscriberAdmin(admin.ModelAdmin):
    list_display = ('email', 'subscribed_at')
    search_fields = ('email',)
    ordering = ('-subscribed_at',)
    list_per_page = 20