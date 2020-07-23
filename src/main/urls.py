"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path
from . import views

from django.contrib.auth import views as auth_views

app_name = "main"

urlpatterns = [
    path('', views.home, name='post-list'),
    
    path('<int:id>', views.post_detail, name='post-detail'),
    path('post_create/', views.post_create, name='post_create'),
    path('<int:id>/update/', views.post_update, name='post-update'),
    path('<int:id>/delete/', views.post_delete, name='post-delete'),
    path('<slug:single_slug>', views.post_sort, name='post-sort'),
    path('<int:id>/like/', views.post_like, name='post-like'),
    path('about/', views.about, name='about'),

]
