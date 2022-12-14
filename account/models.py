import random

from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
# Create your models here.

class CustomUserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    def _create_user(self, phone,email, password , **extra_fields):
        """Create and save a User with the given email and password."""
        if not phone:
            raise ValueError('The given phone must be set')

        email = self.normalize_email(email)
        user = self.model(phone=phone,email=email,password=password, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, phone,email, password, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(phone,email, password, **extra_fields)

    def create_superuser(self, phone,email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(phone,email, password, **extra_fields)

class CustomUser(AbstractUser):
    username=models.CharField(max_length=15,blank=True)
    phone=models.CharField(max_length=12,unique=True)

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['email']
    objects = CustomUserManager()


class Profile(models.Model):
    owner=models.OneToOneField(CustomUser,on_delete=models.CASCADE,related_name="profile_data")
    Gender=(
        ("male","male"),
        ("female","female"),
        ("other","other"),
        ("not disclosed","not disclosed")
    )
    gender=models.CharField(max_length=20,choices=Gender,default="male",null=False)
    DOB=models.DateField(null=True,blank=True,default=None)
    work_at=models.CharField(null=True,max_length=50,blank=True)
    lives_in=models.CharField(max_length=50,blank=True,null=True)
    date_of_join=models.DateField(auto_now_add=True,blank=False,null=False)
    profile_photo=models.ImageField(upload_to='profile',blank=True)


class followlist(models.Model):
    user=models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    followers=models.ManyToManyField(CustomUser,blank=True,related_name="followers")
    following=models.ManyToManyField(CustomUser,blank=True,related_name="following")

    def __str__(self):
        return f'{self.user.username} followers {self.followers.count()} and following {self.following.count()}'


