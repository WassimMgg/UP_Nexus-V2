from django.urls import path
from . import views

urlpatterns = [
    path('', views.article_list, name='news'), 
    path('add/', views.article_create, name='article_create'),
    path('<int:pk>/', views.article_detail, name='article_detail'),
    path('<int:pk>/edit/', views.article_update, name='article_update'),
    path('<int:pk>/delete/', views.article_delete, name='article_delete'),
    path('newsletter/subscribe/', views.newsletter_subscribe, name='newsletter_subscribe')
]