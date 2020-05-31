from django.contrib import admin

from .models import User, AccountDetails

admin.site.register(User)
admin.site.register(AccountDetails)
