from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser,BaseUserManager,Group


class CustomManager(BaseUserManager):
    def create_user(self,username=None , password=None, **extra_fields):
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self,username=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(username=username, password=password, **extra_fields)

class CustomUser(AbstractUser):
    username = models.TextField(max_length=200, unique=True)

    REQUIRED_FIELDS = []

    objects = CustomManager()

    class Meta:
        verbose_name='CustomUser'
        verbose_name_plural="CustomUsers"


    groups = models.ManyToManyField(Group, related_name='custom_users')
    user_permissions = models.ManyToManyField('auth.Permission', related_name='custom_user_set', blank=True)

    # groups = models.ManyToManyField('auth.Group', related_name='custom_user_set', blank=True)
    # user_permissions = models.ManyToManyField('auth.Permission', related_name='custom_user_set', blank=True)
