from django.db import models
import jwt
from django.conf import settings
from datetime import datetime, timedelta
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin)
from todo_api.models import TimeStampsModel


class UserManager(BaseUserManager):

    def create_user(self, username, first_name, last_name, email, password=None):
        if first_name is None:
            raise TypeError('Users must have a name')
        if username is None:
            raise TypeError('Users must have an username')
        if email is None:
            raise TypeError('Users must have an email')

        user = self.model(username=username, first_name=first_name, last_name=last_name,
                          email=self.normalize_email(email))
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, username, first_name, last_name, email,  password):
        if password is None:
            raise TypeError('Superusers must have a password.')

        user = self.create_user(username, first_name,
                                last_name, email,  password)
        user.is_superuser = True
        user.is_staff = True
        user.is_active = True
        user.save(using=self._db)

        return user


# Create your models here.

class User(AbstractBaseUser, PermissionsMixin, TimeStampsModel):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=200, db_index=True, unique=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    objects = UserManager()
    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']

    def __str__(self):
        return str(self.username)

    @property
    def token(self):
        return self._generate_jwt_token()

    def _generate_jwt_token(self):
        dt = datetime.now() + timedelta(days=30)
        token = jwt.encode({
            "id": self.pk,
            "exp": int(dt.timestamp())
        }, settings.SECRET_KEY, algorithm='HS256')

        return token.decode('utf-8')
