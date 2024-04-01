import os
from pathlib import Path
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import RegistrationForm, LoginForm
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .token import account_activation_token
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.contrib.auth import get_user_model
from django.urls import reverse
from .forms import ProfileForm
from .models import Profile, CustomUser


def reg_page(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            # Create a profile for the user
            Profile.objects.create(user=user)

            # Send activation email
            current_site = get_current_site(request)
            mail_subject = 'Activation link has been sent to your email id'
            activation_link = reverse('activate', kwargs={'uidb64': urlsafe_base64_encode(
                force_bytes(user.pk)), 'token': account_activation_token.make_token(user)})
            message = render_to_string('api/app_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'activation_link': activation_link,
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()

            messages.success(
                request, "Registration successful. Just confirm your email")
            return redirect('login')
        else:
            return render(request, 'api/registration.html', {'form': form})
    else:
        form = RegistrationForm()
    return render(request, 'api/registration.html', {'form': form})


def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            user = authenticate(
                request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
        else:
            messages.error(request, "Invalid username or password")
    else:
        form = LoginForm()
    return render(request, 'api/login.html', {'form': form})


def home_page(request):
    user = None
    if request.user.is_authenticated:
        user = request.user

    return render(request, 'api/homepage.html', {'user': user})


def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('home')


@login_required
def profile(request):
    if request.method == 'POST':
        user = request.user
        user.first_name = request.POST.get('name')
        user.last_name = request.POST.get('surname')
        user.username = request.POST.get('username')
        user.email = request.POST.get('email')
        user.save()

        profile, created = Profile.objects.get_or_create(user=user)
        profile.phone = request.POST.get('phone')
        profile.address = request.POST.get('city')
        profile.company = request.POST.get('company')
        if request.FILES.get('image'):
            profile.image = request.FILES['image']

        profile.save()

        return redirect('/profile')

    return render(request, 'api/profile.html', {'user': request.user})


def oprder_page(request):
    user = None
    print(request.user.id)
    if request.user.is_authenticated:
        profile = Profile.objects.get(user_id=request.user.id)
        user = CustomUser.objects.get(first_name=request.user.first_name)

    return render(request, 'api/order_page.html', {'user': user})
