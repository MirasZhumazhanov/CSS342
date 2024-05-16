from django.shortcuts import render, HttpResponse
from .models import Booking
from datetime import datetime
import os
from pathlib import Path
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse, JsonResponse
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
from .models import *
from django.db.models import Q


def reg_page(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = True
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
        if 'next' in request.GET:
            messages.info(request, 'You need to log in to access this page.')
        form = LoginForm()
    return render(request, 'api/login.html', {'form': form})


def support_page(request):
    return render(request, 'api/support.html')


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


def foo(request):
    user = None
    print(request.user.id)
    if request.user.is_authenticated:
        user = CustomUser.objects.get(first_name=request.user.first_name)

    return render(request, 'api/booking-page.html', {'user': user})


@login_required
def order_page(request, pk):
    user = request.user if request.user.is_authenticated else None
    billboard = Billboard.objects.get(id=pk)
    bookings = Booking.objects.all()
    print(billboard.image.url)
    return render(request, 'api/order_page.html', {'bill': billboard, 'user': user, 'book': bookings})


def get_bookings(request, pk):
    billboard = get_object_or_404(Billboard, id=pk)
    bookings = Booking.objects.filter(billboard=billboard)

    data = []
    for booking in bookings:
        event = {

            "title": booking.customer.username,
            "start": booking.start_date.strftime('%Y-%m-%d'),
            "end": booking.end_date.strftime('%Y-%m-%d'),

        }

        data.append(event)
    return JsonResponse(data, safe=False)


# def check_overlapping_bookings(request):
#     start_date = request.GET.get('start_date')
#     end_date = request.GET.get('end_date')

#     overlapping_bookings = Booking.objects.filter(
#         start_date__lte=end_date,
#         end_date__gte=start_date
#     ).exists()

#     return JsonResponse({'overlapping': overlapping_bookings})


def add_event(request):
    start = request.GET.get("start", None)
    end = request.GET.get("end", None)
    billboard_id = request.GET.get('billboard_id', None)
    user_id = request.GET.get('user_id', None)

    overlapping_bookings = Booking.objects.filter(
        Q(start_date__lte=end) & Q(end_date__gte=start) & Q(billboard_id=billboard_id))
    if not overlapping_bookings.exists():
        # Convert start and end dates to datetime objects
        start_date = datetime.strptime(start, '%Y-%m-%d')
        end_date = datetime.strptime(end, '%Y-%m-%d')

        # Calculate duration in days
        days = (end_date - start_date).days

        # Calculate total cost
        cost_per_day = 20000  # Example cost per day
        total_cost = cost_per_day * days

        # Create and save the booking
        booking = Booking.objects.create(
            customer_id=user_id,
            billboard_id=billboard_id,
            start_date=start_date,
            end_date=end_date,
            total_cost=total_cost
        )

        # Optionally, you can return the ID of the created booking along with the total cost
        data = {
            'success': True,
            'message': 'Successfully added booking.',
            'total_cost': total_cost,
            'booking_id': booking.id  # Optionally, include the ID of the created booking
        }
    else:
        data = {
            'success': False,
            'message': 'There are overlapping bookings for the selected dates.'
        }
    return JsonResponse(data)


def status(request):
    user_bookings = Booking.objects.filter(
        customer=request.user).order_by('-id')
    return render(request, 'api/status.html', {'user_bookings': user_bookings})


@login_required
def search_billboards(request):
    # Retrieve all Billboard objects from the database
    billboards = Billboard.objects.all()

    # Assuming you have retrieved the required data for rendering the template
    # For example, billboards and profileId
    context = {
        'billboards': billboards,
    }
    return render(request, 'api/search.html', context)

# views.py


def payment(request):
    # Retrieve the last booking if it exists
    last_booking = Booking.objects.last()

    # Initialize total_price with a default value
    total_price = 0

    # Check if last_booking is not None
    if last_booking:
        total_price = last_booking.total_cost

    if request.method == 'POST':
        # Handle form submission
        first_name = request.POST.get('first_name', '')
        last_name = request.POST.get('last_name', '')
        email = request.POST.get('email', '')
        card_number = request.POST.get('card_number', '')
        expiry_date = request.POST.get('expiry_date', '')
        cvc = request.POST.get('cvc', '')
        cardholder_name = request.POST.get('cardholder_name', '')

        # Here, you would typically validate the form data and process the payment
        # For simplicity, let's just print the data for now
        print("First Name:", first_name)
        print("Last Name:", last_name)
        print("Email:", email)
        print("Card Number:", card_number)
        print("Expiry Date:", expiry_date)
        print("CVC:", cvc)
        print("Cardholder Name:", cardholder_name)

        # You might want to redirect the user to a thank you page or some other page
        return HttpResponse("Payment Successful!")
    else:
        # If it's not a POST request, just render the payment page
        return render(request, 'api/payment.html', {'total_price': total_price})
