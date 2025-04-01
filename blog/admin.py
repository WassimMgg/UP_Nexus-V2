from django.contrib import admin
from .models import Post

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'status', 'date_posted', 'requester')
    list_filter = ('status', 'date_posted')
    search_fields = ('title', 'author__username', 'requester__username')
    actions = ['approve_selected_posts', 'reject_selected_posts']

    def approve_selected_posts(self, request, queryset):
        queryset.update(status='approved')
    approve_selected_posts.short_description = "Approve selected posts"

    def reject_selected_posts(self, request, queryset):
        queryset.update(status='rejected')
    reject_selected_posts.short_description = "Reject selected posts"