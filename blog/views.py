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
from users.views import public_profile
from django.contrib.auth.models import User
from django.db.models import Q


def home(request):
    posts = Post.objects.all().order_by('-date_posted')
    return render(request, 'blog/home.html', {'title': 'Home', 'posts': posts})



def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/PostDeatails.html', {'post': post})

@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post-detail', pk=post.pk)
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
    announce = Post.objects.all()
    return render(request, 'blog/announcement.html', {'title': 'Announcement', 'posts': announce})

def search(request):
    search_term = request.GET.get('search', '')
    selected_roles = request.GET.getlist('roles')

    # Start with base queryset excluding empty/no roles
    profiles = Profile.objects.exclude(
        Q(role__exact='') | Q(role__isnull=True)
    )
    
    if search_term:
        profiles = profiles.filter(
            Q(user__username__icontains=search_term) |
            Q(user__first_name__icontains=search_term) |
            Q(user__last_name__icontains=search_term)
        )
            
    if selected_roles:
        profiles = profiles.filter(role__in=selected_roles)

    context = {
        'profiles': profiles,
        'search_term': search_term,
        'selected_roles': selected_roles,
        'role_choices': Profile.ROLE_CHOICES
    }
    return render(request, 'blog/search.html', context)

