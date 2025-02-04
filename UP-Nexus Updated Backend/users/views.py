from django.shortcuts import render, redirect ,get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import login, authenticate
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
from django.http import HttpResponseRedirect
from .models import  RoleRequest, Profile
from django.core.files.uploadedfile import InMemoryUploadedFile, TemporaryUploadedFile

def login_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('blog-home'))

    if request.method == 'POST':
        username = request.POST.get('username')  # Use .get() to avoid KeyError
        password = request.POST.get('password')  # Use .get() to avoid KeyError

        if username and password:  # Ensure both fields are provided
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse('blog-home'))
            else:
                return render(request, 'users/Login_Page.html', {'error': 'Invalid username or password'})
        else:
            return render(request, 'users/Login_Page.html', {'error': 'Username and password are required'})
    else:
        return render(request, 'users/Login_Page.html')
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()  # Save the user and profile
            login(request, user)  # Log the user in after registration
            messages.success(request, 'Your account has been created! You are now logged in.')
            return redirect('role-selection')  # Redirect to the home page or another page
        else:
            # Print form errors for debugging
            print(form.errors)
            messages.error(request, 'There was an error with your registration. Please check the form.')
    else:
        form = UserRegisterForm()
    
    # Pass the form to the template for rendering
    return render(request, 'users/Login_Page.html', {'form': form})

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
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    return render(request, 'users/UserProfile.html', {
        'u_form': u_form,
        'p_form': p_form,
    })


@staff_member_required
def approve_role(request, role_request_id):
    role_request = get_object_or_404(RoleRequest, id=role_request_id)

    # Get the user's profile
    profile = Profile.objects.get(user=role_request.user)

    # Assign the approved role
    profile.role = role_request.role
    profile.is_verified = True

    # Transfer role-specific data from RoleRequest to Profile (excluding files)
    for field, value in role_request.role_specific_data.items():
        if hasattr(profile, field):  # Ensure the field exists in Profile
            setattr(profile, field, value)

    profile.save()

    # Update RoleRequest status
    role_request.status = "approved"
    role_request.save()

    messages.success(request, f"Role '{role_request.role}' has been assigned to {role_request.user.username}.")

    return redirect(reverse("admin:users_rolerequest_changelist"))


@staff_member_required
def reject_role(request, role_request_id):
    role_request = get_object_or_404(RoleRequest, id=role_request_id)

    # Reject the role request
    role_request.status = "rejected"
    role_request.save()

    # Show success message in Django admin
    messages.warning(request, f"Role request for {role_request.user.username} has been rejected.")

    # Redirect to the RoleRequest list in Django Admin
    return redirect(reverse("admin:users_rolerequest_changelist"))

@staff_member_required
def admin_role_requests(request):
    role_requests = RoleRequest.objects.all()
    return render(request, 'admin/role_requests.html', {'role_requests': role_requests})