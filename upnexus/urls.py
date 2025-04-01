"""django_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from users import views as user_views
from blog import views as blog_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', user_views.register, name='register'),
    path('login/', user_views.login_view, name='login'),
    path('profile/', user_views.profile, name='profile'),
    path('profile/<str:username>/', user_views.public_profile, name='public-profile'),
    path('ecosystem/', user_views.ecosystem, name='ecosystem'),
    path('avatar-upload/', user_views.avatar_upload, name='avatar_upload'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('', include('blog.urls')),
    path('role-selection/', user_views.role_selection, name='role-selection'),
    path('verification-<str:role>/', user_views.role_specific_verification, name='role-specific-verification'),
    path('approve-role-request/<int:role_request_id>/', user_views.approve_role, name='approve_role_request'),
    path('reject-role-request/<int:role_request_id>/', user_views.reject_role, name='reject_role_request'),
    path('search/', blog_views.search, name='search'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


