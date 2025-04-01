from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Post 
from users.models import Profile
from .forms import PostForm  
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Q


def home(request):
    posts = Post.objects.all().order_by('-date_posted')
    return render(request, 'blog/home.html', {'title': 'Home', 'posts': posts})



def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/PostDeatails.html', {'post': post})

@login_required
def post_create(request):
    # Check if user has a verified role
    try:
        profile = request.user.profile
        if not profile.is_verified or not profile.role:
            raise PermissionDenied
    except Profile.DoesNotExist:
        raise PermissionDenied

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            # Create post but don't publish immediately
            post = form.save(commit=False)
            post.author = request.user
            post.status = 'pending'  # Set status here
            post.save()

            messages.info(request, 'Your post has been submitted for admin approval.')
            return redirect('blog-home')
    else:
        form = PostForm()

    return render(request, 'blog/AddEventPage.html', {'form': form})

@login_required
def post_update(request, pk):
    
    post = get_object_or_404(Post, pk=pk)
    
    if request.method == "POST":
      
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
           
            return redirect('post-detail', pk=post.pk)
    else:
      
        form = PostForm(instance=post)
    
    context = {
        'post': post,
        'form': form,
    }
    return render(request, 'blog/EditPostPage.html', context)

@login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.user != post.author:
        raise PermissionDenied
    
    if request.method == 'POST':
        post.delete()
        return redirect('announcement')
    return render(request, 'blog/post_confirm_delete.html', {'post': post})


@login_required
def announcement(request):
    approved_posts = Post.objects.filter(status='approved').order_by('-date_posted')
    return render(request, 'blog/announcement.html', {'title': 'Announcement', 'posts': approved_posts})

@staff_member_required
def approve_post(request, post_request_id):
    post_request = get_object_or_404(Post, id=post_request_id)
    post_request.status = 'approved'
    post_request.save()

    # Update the Post's status directly
    post = post_request.post
    post.status = 'approved'
    post.save()

    messages.success(request, f"Post '{post.title}' has been approved.")
    return redirect('admin_post_requests')


@staff_member_required
def reject_post(request, post_request_id):
    post_request = get_object_or_404(Post, id=post_request_id)
    post_request.status = 'rejected'
    post_request.save()

    messages.warning(request, f"Post '{post_request.post.title}' has been rejected.")
    return redirect('admin_post_requests')


@staff_member_required
def admin_post_requests(request):
    post_requests = Post.objects.filter(status='pending').select_related('post')
    return render(request, 'admin/post_requests.html', {'post_requests': post_requests})
@login_required
def search(request):
    search_term = request.GET.get('search', '')
    selected_roles = request.GET.getlist('roles')

    # Start with base queryset excluding empty/no roles
    profiles = Profile.objects.exclude(
        Q(role__exact='User') | Q(role__isnull=True)
    )
    
    if search_term:
        profiles = profiles.filter(
            Q(user__username__icontains=search_term) |
            Q(user__first_name__icontains=search_term) |
            Q(user__last_name__icontains=search_term)
        )
            
    if selected_roles:
        profiles = profiles.filter(role__in=selected_roles)
    profile_role = Profile.ROLE_CHOICES
    profile_role = profile_role[1:]
    context = {
        'profiles': profiles,
        'search_term': search_term,
        'selected_roles': selected_roles,
        'role_choices':  profile_role
    }
    return render(request, 'blog/search.html', context)

