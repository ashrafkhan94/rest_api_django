from django.db import models

""" Overriding & Customizing django Default models """
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import UserManager


class UserProfileManager(UserManager):
    """Manager if user profiles"""

    def create_user(self, username, email, password=None):
        """Create a new user profile"""
        if not email:
            raise ValueError('Email should be present')

        email = self.normalize_email(email)
        user = self.model(email=email, name=username)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, username, email, password):
        """Create an admin user"""

        user = self.create_user(username, email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save(self._db)

        return user


class UserProfile(AbstractUser, PermissionsMixin):
    """Database model for users in the system"""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserProfileManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def get_full_name(self):
        """Retrieve fullname of user"""
        return self.name

    def get_short_name(self):
        """Retreive shortname of user"""
        return self.name

    def __str__(self):
        return self.email

