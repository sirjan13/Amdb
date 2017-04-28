from __future__ import unicode_literals
from django.db import models

# Create your models here.


class Users(models.Model):
    name = models.CharField(max_length=300, null=False, blank=False)
    username = models.CharField(max_length=120, null=False, blank=False, unique=True)
    password = models.CharField(max_length=100, null=False, blank=False)
    short_bio = models.CharField(max_length=350)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

