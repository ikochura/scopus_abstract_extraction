from django.contrib import admin

from .models import Category, Dataset

# Register your models here.

admin.site.register(Category)
admin.site.register(Dataset)
