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
from django.urls import path, reverse_lazy
from . import views
from django.contrib.auth import views as auth_views


app_name = "account"

urlpatterns = [
    path('<str:username>', views.account_view, name='account'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # built-in password reset class views
    path('password_reset/', auth_views.PasswordResetView.as_view(
            template_name='password_reset/password_reset_form.html', 
            email_template_name='password_reset/password_reset_email.html',
            subject_template_name='password_reset/password_reset_subject.txt',
            success_url=reverse_lazy('account:password_reset_done'),
            ),
        name="password_reset"
        ),

    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(
            template_name='password_reset/password_reset_done.html',
            ),
        name="password_reset_done"
        ),

    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
            template_name='password_reset/password_reset_confirm.html',
            success_url=reverse_lazy('account:password_reset_complete'),
            ),
        name="password_reset_confirm"
        ),

    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='password_reset/password_reset_complete.html',
            ),
        name="password_reset_complete"
        ),
]
