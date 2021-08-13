from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import MyUserAccountManager

# Create your models here.

class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, help_text='Enter Email Address')
    app_id = models.CharField(max_length=50, unique=True, help_text='Enter App ID')
    secret_id = models.CharField(max_length=50, unique=True, help_text='Enter Secret ID')
    profile_picture = models.ImageField(upload_to='user_profile')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = MyUserAccountManager() # To set our custom account manager as base manager

    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def __str__(self) -> str:
        return f'{self.email} - {self.first_name} {self.last_name}'

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True