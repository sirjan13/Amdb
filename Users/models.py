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


#  This Model Holds information regarding different Movies
class Movie(models.Model):
    name = models.CharField(max_length=300)
    release_date = models.DateTimeField()
    overall_rating = models.DecimalField(decimal_places=2, max_digits=4, default=0.0)
    censor_board_rating = models.CharField(max_length=5)
    duration_in_minutes = models.IntegerField(default=180)
    poster_picture_url = models.CharField(max_length=300)
    user = models.ForeignKey(Users)


#  stores movie genres
class Genre(models.Model):
    name = models.CharField(max_length=255)


#  Mapping table to Genre and movies ie one to many mapping
class MovieGenre(models.Model):
    movie = models.ForeignKey(Movie)
    genre = models.ForeignKey(Genre)


#  to store user reviews and ratings
class Review(models.Model):
    movie = models.ForeignKey(Movie)
    user = models.ForeignKey(Users)
    rating = models.DecimalField(decimal_places=2, max_digits=3, default=0.0)
    review = models.CharField(max_length=300)


