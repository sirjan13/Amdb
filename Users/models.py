from __future__ import unicode_literals
from django.db import models
from uuid import uuid4
# Create your models here.


class Users(models.Model):
    name = models.CharField(max_length=300, null=False, blank=False)
    username = models.CharField(max_length=120, null=False, blank=False, unique=True)
    password = models.CharField(max_length=100, null=False, blank=False)
    short_bio = models.CharField(max_length=350)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)


class AccessToken(models.Model):
    user = models.ForeignKey(Users)
    access_token = models.CharField(max_length=300)
    is_valid = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True)
    last_request_on = models.DateTimeField(auto_now=True)

    def generate_access_token(self):
        self.access_token = uuid4()
