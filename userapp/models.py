from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.validators import RegexValidator

# Create your models here.
class AccountManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email is required')
        
        user = self.model(email=self.normalize_email(email),**extra_fields)
        user.set_password(password)
        user.save(self._db)
        
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_admin', True)

        if extra_fields.get('is_active') is not True:
            raise ValueError('Superuser field is_active must be true')

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser field is_staff must be true')
        
        if extra_fields.get('is_admin') is not True:
            raise ValueError('Superuser field is_admin must be True')
        
        return self.create_user(email=email, password=password, **extra_fields)
    

class User(AbstractBaseUser):
    email = models.EmailField(max_length=100, unique=True)
    password = models.CharField(max_length=250)
    name = models.CharField(max_length=50, null=True)
    phone_regex = RegexValidator(regex=r'^\d+$', message="Mobile number should only contain digits")
    phone = models.PositiveBigIntegerField(null=True, validators=[phone_regex])
    profile_image = models.ImageField(upload_to='profile_image', null=True, blank=True)
    date_joined = models.DateField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_owner=models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)  # Set to True by default for regular users
    business_name = models.CharField(max_length=100, null=True)  # Theater owner's business name
    business_address = models.CharField(max_length=250, null=True)  # Address of the theater
    business_license_number = models.CharField(max_length=50, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = AccountManager()

    def get_full_name(self):
        return self.name

    def get_short_name(self):
        return self.name

    def __str__(self):
        return self.email
    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, add_label):
        return True