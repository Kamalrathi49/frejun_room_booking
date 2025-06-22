# std imports
from datetime import date

# django imports
from django.db import models
from django.contrib.auth.models import AbstractUser
from model_utils import Choices
from django.utils.translation import gettext_lazy as _

# local imports
from apps.core.mixins import StatusMixin, EmailMixin, UUIDMixin


class User(AbstractUser, StatusMixin, EmailMixin, UUIDMixin):
    """
    Default custom user model.
    """
    MALE = 'male'
    FEMALE = 'female'
    OTHER = 'other'
    GENDER_CHOICES = Choices(
        (MALE, 'Male'),
        (FEMALE, 'Female'),
        (OTHER, 'Others')
    )

    gender = models.CharField(choices=GENDER_CHOICES, max_length=6, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    
    USERNAME_FIELD = 'username'
    
    def is_child(self):
        if self.date_of_birth:
            today = date.today()
            age = today.year - self.date_of_birth.year - (
                (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day)
            )
            return age < 10
        return False