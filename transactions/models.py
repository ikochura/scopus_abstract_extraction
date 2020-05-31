from django.conf import settings
from django.db import models

User = settings.AUTH_USER_MODEL


class Category(models.Model):
    name_group_dataset = models.CharField(
        max_length=30,
    )
    timestamp = models.DateTimeField(auto_now_add=True)

    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             )

    def __str__(self):
        return str(self.user)


class Dataset(models.Model):
    scopus_id = models.CharField(max_length=50)
    abstract = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category,
                                 on_delete=models.CASCADE,
                                 )

    def __str__(self):
        return str(self.category)
