from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils import timezone

class MovienetUserManager(BaseUserManager):
    def create_user(self, email, date_of_birth, sex, first_name, last_name, 
                    username, password=None):
        """
        Creates and saves a User with the given email, date of
        birth, sex and password.
        """
        if not username:
            raise ValueError('Users must have a username')
        elif not email:
            raise ValueError('Users must have an email address')
        elif not date_of_birth:
            raise ValueError('Users must have a date of birth')
        elif not sex:
            raise ValueError('Users must have a valid sex')
        elif not first_name or not last_name:
            raise ValueError('Users must have a full name')

        now = timezone.now()

        user = self.model(
            username=username,
            email=MovienetUserManager.normalize_email(email),
            date_of_birth=date_of_birth,
            sex=sex,
            first_name=first_name,
            last_name=last_name,
            is_staff=False, is_active=True, is_superuser=False,
            last_login=now, date_joined=now
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, date_of_birth, sex, first_name, last_name, 
                         username, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        u = self.create_user(email,
            username=username,
            password=password,
            date_of_birth=date_of_birth,
            first_name=first_name, last_name=last_name,
            sex=sex
        )
        u.is_staff = True
        u.is_active = True
        u.is_superuser = True
        u.save(using=self._db)
        return u

class MovienetUser(AbstractUser):    
    SEX_CHOICES = (('M', 'Male'), ('F', 'Female'))
    sex = models.CharField(max_length=1, choices=SEX_CHOICES)
    date_of_birth = models.DateField()
    REQUIRED_FIELDS = ['first_name', 'last_name', 'date_of_birth', 'sex', 'email']
    objects = MovienetUserManager()
    