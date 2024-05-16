from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.core.validators import RegexValidator
from django import forms
from django.contrib.auth.models import User
from django.conf import settings


class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, username, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=150, unique=True)
    username = models.CharField(max_length=150, unique=True)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    phone_number = models.CharField(
        max_length=20, unique=True, null=True, blank=True)
    last_login = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username


class NumericPhoneField(models.CharField):
    description = "A phone number containing only numeric characters"

    def formfield(self, **kwargs):
        # Apply a regular expression validator to allow only numeric characters
        numeric_validator = RegexValidator(
            r'^[0-9]+$', 'Only numeric characters are allowed.')

        # Include JavaScript to enforce numeric input on the client side
        kwargs['widget'] = forms.TextInput(
            attrs={'pattern': '[0-9]*', 'title': 'Please enter only numeric characters'})
        kwargs['validators'] = [numeric_validator]

        return super().formfield(**kwargs)


def user_directory_path(instance, filename):
    # File will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'user_{0}/{1}'.format(instance.user.id, filename)


class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, blank=True)
    address = models.CharField(max_length=100, blank=True)
    company = models.CharField(max_length=100, blank=True)
    image = models.ImageField(
        upload_to='profile_images', default='profile_images/acc.png')


class Billboard(models.Model):
    SIZE_CHOICES = [
        ('Small', 'Small'),
        ('Medium', 'Medium'),
        ('Large', 'Large'),
    ]
    CATEGORY_TYPES = [
        ('Traditional Static', 'Traditional Static'),
        ('Digital', 'Digital'),
        ('Mobile', 'Mobile'),
    ]

    type = models.CharField(max_length=100, choices=CATEGORY_TYPES, blank=True)
    category = models.CharField(
        max_length=50, choices=SIZE_CHOICES, blank=True)
    address = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100, blank=True)
    image = models.ImageField(upload_to='billboard_images/', blank=True)
    district = models.CharField(max_length=120, blank=True)
    size = models.CharField(max_length=200, blank=True)
    price = models.CharField(max_length=200, blank=True)

    def __str__(self) -> str:
        return self.address


class Booking(models.Model):
    STATUS_CHOICES = [
        ('In progress', 'In progress'),
        ('Canceled', 'Canceled'),
        ('Approved', 'Approved'),
    ]

    customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    billboard = models.ForeignKey(Billboard, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    total_cost = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True)
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='In progress')

    def __str__(self) -> str:
        return self.customer.username + ' | ' + self.status


class Review(models.Model):
    customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)
    comment = models.TextField(blank=True)
