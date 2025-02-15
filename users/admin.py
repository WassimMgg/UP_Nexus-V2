from django.contrib import admin
from .models import Profile, RoleRequest
from django.db import models
from django.utils.html import format_html
from django.urls import reverse
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'pending_role', 'is_verified')
    list_filter = ('role', 'is_verified')
    search_fields = ('user__username', 'company_name', 'incubator_name', 'accelerator_name', 'project_name')
    readonly_fields = ('user', 'role', 'pending_role', 'company_name', 'business_license', 'skills', 'portfolio_link', 'resume',
                       'incubator_name', 'incubator_description', 'incubator_certificate', 'accelerator_name', 'accelerator_description',
                       'accelerator_certificate', 'investment_focus', 'investment_stage', 'investor_certificate', 'project_name',
                       'project_description', 'project_proposal')
    actions = ['approve_role']

    def approve_role(self, request, queryset):
        queryset.update(is_verified=True, role=models.F('pending_role'))
    approve_role.short_description = "Approve selected roles"

    def has_add_permission(self, request):
        return False  # Disable adding new profiles from the admin panel

@admin.register(RoleRequest)
class RoleRequestAdmin(admin.ModelAdmin):
    list_display = (
    'user', 'role', 'status', 'created_at', 'role_specific_data_display', 'file_attachments', 'approve_button',
    'reject_button')
    list_filter = ('status', 'role')
    actions = ['approve_requests', 'reject_requests']

    def role_specific_data_display(self, obj):
        """Format role-specific data nicely."""
        if obj.role_specific_data:
            formatted_data = "".join(
                f"<li><strong>{key}:</strong> {value}</li>"
                for key, value in obj.role_specific_data.items()
            )
            return format_html(f"<ul>{formatted_data}</ul>")
        return "No Data"

    role_specific_data_display.short_description = "Role Specific Data"

    def file_attachments(self, obj):
        """Display file links for verification documents."""
        file_fields = {
            'business_license': 'Business License',
            'resume': 'Resume',
            'incubator_certificate': 'Incubator Certificate',
            'accelerator_certificate': 'Accelerator Certificate',
            'investor_certificate': 'Investor Certificate',
            'project_proposal': 'Project Proposal'
        }

        files_html = ""
        for field, label in file_fields.items():
            file = getattr(obj.user.profile, field, None)
            if file:
                files_html += f'<li><strong>{label}:</strong> <a href="{file.url}" target="_blank">Download</a></li>'

        return format_html(f"<ul>{files_html}</ul>") if files_html else "No Attachments"

    file_attachments.short_description = "File Attachments"

    def approve_button(self, obj):
        if obj.status == 'pending':
            url = reverse('approve_role_request', args=[obj.id])
            return format_html('<a class="button" href="{}">Approve</a>', url)
        return "Approved"

    def reject_button(self, obj):
        if obj.status == 'pending':
            url = reverse('reject_role_request', args=[obj.id])
            return format_html('<a class="button" href="{}">Reject</a>', url)
        return "Rejected"

    approve_button.short_description = "Approve"
    reject_button.short_description = "Reject"

    def approve_requests(self, request, queryset):
        """Bulk approve selected requests."""
        for obj in queryset:
            obj.status = "approved"
            obj.user.profile.role = obj.role  # Assign role
            obj.user.profile.is_verified = True  # Mark verified
            obj.user.profile.save()
            obj.save()
        self.message_user(request, "Selected requests have been approved.")

    def reject_requests(self, request, queryset):
        """Bulk reject selected requests."""
        queryset.update(status="rejected")
        self.message_user(request, "Selected requests have been rejected.")
