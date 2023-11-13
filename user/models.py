from django.db import models
from django.contrib.auth.models import User as BaseUser,AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
# from django.contrib.auth.hashers import make_password

class BaseUserManager(BaseUserManager):
    
    def create_user(self, username, password=None, dob=None, **extra_fields):
        if not username:
            raise ValueError('The username field must be set')

        user = self.model(username=username, dob=dob, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, dob=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(username, password, dob, **extra_fields)

class BaseUser(AbstractBaseUser, PermissionsMixin):
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other')
    ]

    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    phonenumber = models.CharField(max_length=10)
    dob = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=20, choices=GENDER_CHOICES)
    address = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=30, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    photo = models.ImageField(upload_to='media/user_images/', blank=True, null=True)
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']
    
    objects = BaseUserManager()

    def __str__(self):
        return f"{self.firstname} {self.lastname}"
