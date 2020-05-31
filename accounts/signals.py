from django.db.models import Max
from django.db.models.signals import pre_save
from django.dispatch import receiver

from .models import User, AccountDetails

