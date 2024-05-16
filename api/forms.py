from django import forms
from .models import CustomUser
from django.contrib.auth.forms import AuthenticationForm
from django.db import IntegrityError
from django.db import models
from .models import Profile


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password1 = forms.CharField(widget=forms.PasswordInput)
    email = forms.CharField()

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email',
                  'username', 'password', 'phone_number']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        try:
            CustomUser.objects.get(email=email)
            raise forms.ValidationError('This email is already in use')
        except CustomUser.DoesNotExist:
            pass
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username')
        try:
            CustomUser.objects.get(username=username)
            raise forms.ValidationError(
                'This username has already been taken.')
        except CustomUser.DoesNotExist:
            pass
        return username

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        password = self.cleaned_data.get('password')

        if password1 != password:
            raise forms.ValidationError("Passwords don't match")
        return password1

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class LoginForm(AuthenticationForm):

    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Password'}))


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['phone', 'address', 'company', 'image']
