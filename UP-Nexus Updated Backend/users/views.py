from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.urls import reverse
from .forms import (
    UserRegisterForm,
    UserUpdateForm,
    ProfileUpdateForm,
    StartupVerificationForm,
    FreelancerVerificationForm,
    IncubatorVerificationForm,
    AcceleratorVerificationForm,
    InvestorVerificationForm,
    ProjectHolderVerificationForm
)
from .models import Profile, RoleRequest
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            login(request, user)
            messages.success(request, f'Your account has been created! Choose your role or skip.')
            return redirect('role-selection')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})

def role_selection(request):
    if request.method == 'POST':
        selected_role = request.POST.get('role')
        if selected_role:
            request.user.profile.pending_role = selected_role
            request.user.profile.save()
            role_request = RoleRequest.objects.create(
                user=request.user,
                role=selected_role,
                status='pending')
            # Redirect to the role-specific verification page
            return redirect(reverse('role-specific-verification', args=[selected_role]))

        return redirect('blog-home')  # If skipped, redirect to the homepage

    return render(request, 'users/role_selection.html')

from django.core.files.uploadedfile import InMemoryUploadedFile, TemporaryUploadedFile

from django.core.files.uploadedfile import InMemoryUploadedFile, TemporaryUploadedFile

@login_required
def role_specific_verification(request, role):
    profile = request.user.profile
    form_class = None

    if role == 'startup':
        form_class = StartupVerificationForm
    elif role == 'freelancer':
        form_class = FreelancerVerificationForm
    elif role == 'incubator':
        form_class = IncubatorVerificationForm
    elif role == 'accelerator':
        form_class = AcceleratorVerificationForm
    elif role == 'investor':
        form_class = InvestorVerificationForm
    elif role == 'project_holder':
        form_class = ProjectHolderVerificationForm
    else:
        return redirect('profile')

    if request.method == 'POST':
        form = form_class(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            # Save the form data to the profile
            form.save()

            # Extract non-file data for role_specific_data
            role_specific_data = {}
            for field, value in form.cleaned_data.items():
                if not isinstance(value, (InMemoryUploadedFile, TemporaryUploadedFile)):
                    role_specific_data[field] = value

            # Update the RoleRequest object with role-specific data
            role_request = RoleRequest.objects.filter(user=request.user, role=role, status='pending').latest('created_at')
            role_request.role_specific_data = role_specific_data
            role_request.save()

            messages.success(request, f'Your {role} verification request has been submitted successfully.')
            return redirect('profile')
    else:
        form = form_class(instance=profile)

    return render(request, f'users/verification_{role}.html', {'form': form, 'role': role})

@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form,
    }
    return render(request, 'users/profile.html', context)