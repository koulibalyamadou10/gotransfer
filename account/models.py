import uuid

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('You did not enter a valid email address.')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)

# Contient les informations des utilisateurs du système.
class CustomUser(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=50, blank=False, null=False)
    last_name = models.CharField(max_length=50, blank=False, null=False)
    email = models.EmailField(unique=True, blank=False, null=False, error_messages={
        'unique': 'Ce mail existe deja !'
    })
    role = models.CharField(
        max_length=20, 
        choices=[
            ('customer', 'Client'),
            ('agent', 'Agent'),
        ], 
        default="customer"
    )
    phone_number = models.CharField(max_length=13, blank=False, null=False)
    address = models.TextField(blank=False, null=False)
    bio = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='images/', default='image.png')
    user_uuid = models.UUIDField(default=uuid.uuid4)

    card = models.FileField(upload_to='cards/', blank=True, null=True)
    card_exp_date = models.DateTimeField(blank=True, null=True)

    sponsor_email = models.EmailField(max_length=191, blank=True, null=True)
    balance = models.DecimalField(max_digits=18, decimal_places=2, default=0.00)
    currency = models.CharField(max_length=191, default='CAD')
    commission = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)

    api_token = models.CharField(max_length=191, blank=True, null=True)
    remember_token = models.CharField(max_length=191, blank=True, null=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    email_verified_at = models.DateTimeField(null=True, blank=True)
    email_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def _str_(self):
        return f"{self.first_name} {self.last_name} {self.email} {self.role}"