from django.contrib import admin
from .models import Profile, RoleRequest
from django.db import models
from django.contrib import messages
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
    list_display = ('user', 'role', 'status', 'created_at', 'updated_at')
    list_filter = ('status', 'role')
    search_fields = ('user__username', 'role')
    readonly_fields = ('role_specific_data', 'user', 'role', 'created_at', 'updated_at')
    actions = ['approve_requests', 'reject_requests']

    def approve_requests(self, request, queryset):
        for role_request in queryset:
            role_request.status = 'approved'
            role_request.save()

            # Update the user's profile
            profile = role_request.user.profile
            profile.role = role_request.role
            profile.is_verified = True
            profile.role_request_status = 'approved'

            # Copy role-specific data from RoleRequest to Profile
            role_specific_data = role_request.role_specific_data
            if role_request.role == 'startup':
                profile.company_name = role_specific_data.get('company_name')
                if role_specific_data.get('business_license'):
                    profile.business_license = role_specific_data['business_license']
            elif role_request.role == 'freelancer':
                profile.skills = role_specific_data.get('skills')
                profile.portfolio_link = role_specific_data.get('portfolio_link')
                if role_specific_data.get('resume'):
                    profile.resume = role_specific_data['resume']
            elif role_request.role == 'incubator':
                profile.incubator_name = role_specific_data.get('incubator_name')
                profile.incubator_description = role_specific_data.get('incubator_description')
                if role_specific_data.get('incubator_certificate'):
                    profile.incubator_certificate = role_specific_data['incubator_certificate']
            elif role_request.role == 'accelerator':
                profile.accelerator_name = role_specific_data.get('accelerator_name')
                profile.accelerator_description = role_specific_data.get('accelerator_description')
                if role_specific_data.get('accelerator_certificate'):
                    profile.accelerator_certificate = role_specific_data['accelerator_certificate']
            elif role_request.role == 'investor':
                profile.investment_focus = role_specific_data.get('investment_focus')
                profile.investment_stage = role_specific_data.get('investment_stage')
                if role_specific_data.get('investor_certificate'):
                    profile.investor_certificate = role_specific_data['investor_certificate']
            elif role_request.role == 'project_holder':
                profile.project_name = role_specific_data.get('project_name')
                profile.project_description = role_specific_data.get('project_description')
                if role_specific_data.get('project_proposal'):
                    profile.project_proposal = role_specific_data['project_proposal']

            profile.save()

            # Notify the user
            messages.success(request, f'{role_request.user.username} has been approved for the {role_request.role} role.')

    def reject_requests(self, request, queryset):
        for role_request in queryset:
            role_request.status = 'rejected'
            role_request.save()

            # Update the user's profile
            profile = role_request.user.profile
            profile.role_request_status = 'rejected'
            profile.save()

            # Notify the user
            messages.warning(request, f'{role_request.user.username} has been rejected for the {role_request.role} role.')

    approve_requests.short_description = "Approve selected role requests"
    reject_requests.short_description = "Reject selected role requests"