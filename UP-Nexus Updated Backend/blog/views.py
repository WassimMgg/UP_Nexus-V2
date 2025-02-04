from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Post
from .forms import PostForm  # Assuming you have a form for creating/updating posts

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
    # Retrieve the post instance or return a 404 if not found
    post = get_object_or_404(Post, pk=pk)
    
    if request.method == "POST":
        # Bind data (and files) to the form with the existing post instance
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            # Redirect to the post detail page (adjust URL name/arguments as needed)
            return redirect('post-detail', pk=post.pk)
    else:
        # For a GET request, create a form pre-populated with the post instance
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