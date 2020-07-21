from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth import authenticate
from .models import Account

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = Account
        fields = ("username", "email", "password1", "password2")


class LoginForm(forms.ModelForm):
    password = forms.CharField(max_length=20, widget=forms.PasswordInput)

    class Meta:
        model = Account
        fields = ('email', 'password')

    
    def clean(self):
        if self.is_valid():
            email = self.cleaned_data.get('email')
            password = self.cleaned_data.get('password')
            if not authenticate(email=email, password=password):
                raise forms.ValidationError('Incorrect email or password!')


class UpdateAccountForm(forms.ModelForm):
    class Meta:
         model = Account
         fields = ('email', 'username')

    def clean_email(self):
        if self.is_valid():
            email = self.cleaned_data.get('email')
            try:
                account = Account.objects.exclude(pk=self.instance.pk).get(email=email)
            except Account.DoesNotExist:
                return email
            raise forms.ValidationError(f'Email {email} already exists')

    def clean_username(self):
        if self.is_valid():
            username = self.cleaned_data.get('username')
            try:
                account = Account.objects.exclude(pk=self.instance.pk).get(username=username)
            except Account.DoesNotExist:
                return username
            raise forms.ValidationError(f'Username {username} already exists')
