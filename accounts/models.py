from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.core.validators import (
    MinValueValidator,
    MaxValueValidator,
    RegexValidator,
)
from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from .managers import UserManager


class User(AbstractUser):
    username = models.CharField(
        _('username'), max_length=30, unique=True, null=True, blank=True,
        help_text=_(
            'Required. 30 characters or fewer. Letters, digits and '
            '@/./+/-/_ only.'
        ),
        validators=[
            RegexValidator(
                r'^[\w.@+-]+$',
                _('Enter a valid username. '
                  'This value may contain only letters, numbers '
                  'and @/./+/-/_ characters.'), 'invalid'),
        ],
        error_messages={
            'unique': _("A user with that username already exists."),
        })
    email = models.EmailField(unique=True, null=False, blank=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = UserManager()

    def __str__(self):
        return self.email

    @property
    def full_name(self):
        return '{} {}'.format(self.first_name, self.last_name)


class AccountDetails(models.Model):
    user = models.OneToOneField(
        User,
        related_name='account',
        on_delete=models.CASCADE,
    )
    email = models.EmailField(
        unique=True, null=False, blank=False
    )

    def __str__(self):
        return str(self.email)
