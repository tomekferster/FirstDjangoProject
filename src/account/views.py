from .forms import RegisterForm, LoginForm, UpdateAccountForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Account
from django.http import HttpResponse


def register(request):
    form = RegisterForm(request.POST or None)               # this form returns User so I could use 'user = form.save()' and pass it right to login()
    if form.is_valid():
        print(request.POST)
        form.save()
        email = form.cleaned_data.get('email')
        raw_password = form.cleaned_data.get('password1')
        user = authenticate(email=email, password=raw_password)
        if user is not None:
            messages.success(request, f"{user.username} has been created")
            login(request, user)
            messages.info(request, f'{user.username} is logged in')
            return redirect('main:post-list')
    # else statement not needed, because all the errors are handled by the form itself

    return render(request, 'account/register.html', {'form': form})



def login_view(request):
    # form = AuthenticationForm(request, request.POST or None)
    form = LoginForm(request.POST or None)
    if form.is_valid():
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f" You have successfully logged in as {user.username}")
            return redirect('main:post-list')

    return render(request, 'account/login.html', {'form': form})



def logout_view(request):
    logout(request)
    messages.info(request, 'Logged out successfully')
    return redirect('main:post-list')




def account_view(request, username):
    acc = get_object_or_404(Account, username=username)
    if request.user.username != acc.username and not request.user.is_admin:
        messages.warning(request, "You have no access to other users accounts")
        return redirect(f"/account/{request.user.username}")
    form = UpdateAccountForm(request.POST or None, instance=acc)
    if form.is_valid():
        form.save()
        messages.info(request, f"User ({acc.username}) was updated")
        return redirect('main:post-list')
    
    return render(request, 'account/account.html', {'form': form})
