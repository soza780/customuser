from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, UserManager


# Create your models here.

class CustomUserManager(BaseUserManager):

    def create_user(self, first_name, last_name, email, password):

        if not email:
            raise ValueError('User must have an email address')
        if not first_name:
            raise ValueError('User must have an first name')
        if not last_name:
            raise ValueError('User must have an last name')

        user = self.model(
            email=self.normalize_email(email=email),
            first_name=first_name,
            last_name=last_name,
        )
        user.set_password(raw_password=password)
        user.save(using=self._db)
        return user

    def create_superuser(self, first_name, last_name, email, password):

        user = self.create_user(first_name=first_name, last_name=last_name, email=email)
        user.is_admin = True
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=30, verbose_name='first name')
    last_name = models.CharField(max_length=30, verbose_name='last name')
    email = models.EmailField(max_length=40, verbose_name='email address', unique=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = CustomUserManager()
    REQUIRED_FIELDS = [
        'first_name',
        'last_name',
        'email',
    ]
    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'

    def __str__(self):
        return self.first_name + ' ' + self.last_name
