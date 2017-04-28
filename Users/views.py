from __future__ import unicode_literals
from django.shortcuts import render
from django.http import HttpResponse
from Users.serializers import UserSerializer
from rest_framework.decorators import api_view
from Users.models import Users
from rest_framework.response import Response
# Create your views here.


@api_view(["POST"])
def user_create(request):
    min_password_length = 6
    data = request.data
    name = data['name']
    password = data['password']
    user_name = data['username']
    short_bio = data['short_bio']
    check_valid_username = Users.objects.filter(username=user_name).first()
    if len(name) < 1:
        return Response({'error_description': 'No Name entered'},status=400)
    elif len(password) < min_password_length:
        return Response({'error_description': 'Password should have a minimum of 6 letters'},status=400)
    elif check_valid_username:
        return Response({'error_description': 'Username already exists'},status=400)
    else:
        new_user = Users.objects.create(name=name, username=user_name, password=password, short_bio= short_bio)
        new_user.save()
        return Response(UserSerializer(instance=new_user).data, status=200)