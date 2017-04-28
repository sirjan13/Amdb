from __future__ import unicode_literals
from django.shortcuts import render
from django.http import HttpResponse
from Users.serializers import UserSerializer
from django.contrib.auth.hashers import make_password, check_password
from rest_framework.decorators import api_view
from Users.models import Users,AccessToken
from rest_framework.response import Response
# Create your views here.


@api_view(["POST"])
def user_create(request):
    min_password_length = 6

    data = request.data
    user_name = None
    password = None
    name = None
    short_bio = ""

    if 'username' in request.data:
        user_name = request.data['username']

    if 'password' in request.data:
        password = request.data['password']

    if 'name' in request.data:
        name = request.data['name']

    if 'short_bio' in request.data:
        short_bio = data['short_bio']

    if name is None or len(name) == 0:
        return Response({'error_description': 'No Name entered'}, status=400)

    elif password is None or len(password) < min_password_length:
        return Response({'error_description': 'Password should have a minimum of 6 letters'}, status=400)

    elif user_name is None or len(user_name) == 0:
        return Response({'error_description': 'No UserName Entered'}, status=400)

    check_valid_username = Users.objects.filter(username=user_name).first()

    if check_valid_username:
        return Response({'error_description': 'Username already exists'}, status=400)

    else:
        new_user = Users.objects.create(name=name, username=user_name, password=make_password(password), short_bio=short_bio)
        new_user.save()
        return Response(UserSerializer(instance=new_user).data, status=200)


@api_view(["GET"])
def get_user_details(request):
    if 'user_id' in request.query_params :

        id_provided = request.query_params['user_id']

        if id_provided and len(id_provided) :
            current_user = Users.objects.filter(id=id_provided).first()

            if current_user:
                return Response(UserSerializer(instance=current_user).data, status=200)

        return Response({'error description ': 'No user with id = ' + id_provided + ' was found '}, status=200)

    else:
        all_users = Users.objects.all()
        return Response(UserSerializer(instance=all_users, many=True).data, status=200)


@api_view(["POST"])
def login_user(request):
    username = None
    password = None

    if 'username' in request.data:
        username = request.data['username']

    if 'password' in request.data:
        password = request.data['password']

    if not username or not password :
        return Response({"message": "Invalid request. Username or password not provided."}, status=200)

    current_user = Users.objects.filter(username=username).first()

    if current_user:

        if not check_password(password, current_user.password):
            return Response({'error_description': 'The username Password combination is incorrect '}, status=200)

        token = AccessToken(user=current_user)
        token.generate_access_token()
        token.save()
        return Response({"token": token.access_token}, status=200)
    else:
        return Response({'error_description ': 'Username is Invalid '}, status=200)


