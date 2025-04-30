from django.shortcuts import render, redirect, get_object_or_404
from .models import Article , NewsletterSubscriber
from .forms import ArticleForm , NewsletterSubscriptionForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required


@login_required
def article_list(request):
    # get all articles; client-side JS handles filtering
    articles = Article.objects.all().order_by('-published_date')
    CATEGORY_CHOICES = Article.CATEGORY_CHOICES
    return render(request, 'news/article_list.html', {
        'articles': articles,
        'category_choices': CATEGORY_CHOICES,
    })

@login_required
def article_create(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            print("[DEBUG] Form is valid.")
            article = form.save(commit=False)
            article.author = request.user
            article.save()
            # Debug: print file info and path
            if article.image:
                print(f"[DEBUG] Image saved at: {article.image.path}")
            else:
                print("[DEBUG] No image uploaded.")
            messages.success(request, 'Article created successfully!')
            return redirect('news')
        else:
            print("[DEBUG] Form is invalid.")
            print(form.errors)
            # Render the form with errors
            return render(request, 'news/news_form.html', {'form': form})
    else:
        form = ArticleForm()
    # Always redirect to article_list after GET (prevents resubmission on refresh)
    if request.method == 'GET':
        return render(request, 'news/news_form.html', {'form': form})
    return redirect('news')

@login_required
def article_detail(request, pk):
    article = get_object_or_404(Article, pk=pk)
    return render(request, 'news/news_detail.html', {'article': article})

@login_required
def article_update(request, pk):
    article = get_object_or_404(Article, pk=pk)
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES, instance=article)  # Fixed space between POST and FILES
        if form.is_valid():
            updated_article = form.save()
            messages.success(request, 'Article updated successfully!')
            return redirect('article_detail', pk=updated_article.pk)
    else:
        form = ArticleForm(instance=article)
    return render(request, 'news/news_form.html', {'form': form})

@login_required
def article_delete(request, pk):
    article = get_object_or_404(Article, pk=pk)
    if request.method == 'POST':
        article.delete()
        return redirect('news')
    return render(request, 'news/news_confirm_delete.html', {'object': article})

def newsletter_subscribe(request):
    if request.method == 'POST':
        form = NewsletterSubscriptionForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'Thank you for subscribing to our newsletter!')
            except:
                messages.error(request, 'This email is already subscribed.')
        else:
            messages.error(request, 'Please enter a valid email address.')
    
    return redirect('news')