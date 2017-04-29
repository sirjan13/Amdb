from __future__ import unicode_literals
from django.shortcuts import render
from django.http import HttpResponse
from datetime import datetime
from Users.serializers import UserSerializer,MovieSerializer,ReviewSerializer
from django.contrib.auth.hashers import make_password, check_password
from rest_framework.decorators import api_view
from Users.models import Users,AccessToken,Movie,Genre,MovieGenre,Review
from rest_framework.response import Response
from django.db.models import Avg
# Create your views here.


# to create a new user
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

    elif password is None or len(password) < min_password_length:    # to check if password length is at least 6
        return Response({'error_description': 'Password should have a minimum of 6 letters'}, status=400)

    elif user_name is None or len(user_name) == 0:
        return Response({'error_description': 'No UserName Entered'}, status=400)

    # To check if such a username already exists
    check_valid_username = Users.objects.filter(username=user_name).first()


    if check_valid_username:
        return Response({'error_description': 'Username already exists'}, status=400)

    else:
        new_user = Users.objects.create(name=name, username=user_name, password=make_password(password), short_bio=short_bio)
        new_user.save()
        return Response(UserSerializer(instance=new_user).data, status=200)


# displays details of user passed as query parameter
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

    if not username or not password:    # if either is not present
        return Response({"message": "Invalid request. Username or password not provided."}, status=200)

    current_user = Users.objects.filter(username=username).first()  # check if such a user exists in database

    if current_user:

        if not check_password(password, current_user.password):
            return Response({'error_description': 'The username Password combination is incorrect '}, status=200)

        token = AccessToken(user=current_user)
        token.generate_access_token()
        token.save()
        return Response({"token": token.access_token}, status=200)
    else:
        return Response({'error_description ': 'Username is Invalid '}, status=200)


def check_token_validity(request):
    token_provided = request.META['HTTP_TOKEN']
    validity = AccessToken.objects.filter(access_token=token_provided, is_valid=True).first()

    if validity:
        return validity.user

    return None

@api_view(['POST'])
def create_movie(request):

    #  to check if user is logged in
    logged_in_user = check_token_validity(request)

    if logged_in_user:
        try:
            if 'name' in request.data:
                name = request.data['name']
            else:
                return Response({'error_description ': 'Movie name not provided '}, status=200)

            if 'duration_in_minutes' in request.data:
                duration_in_minutes = int(request.data['duration_in_minutes'])
            else:
                return Response({'error_description ':'Movie Duration not provided '}, status=200)

            if 'release_date' in request.data:
                release_date = datetime.strptime(request.data['release_date'], '%Y-%m-%d')
            else:
                return Response({'error_description ':'Release date not provided '}, status=200)

            if 'censor_board_rating' in request.data:
                censor_board_rating = request.data['censor_board_rating']
            else:
                return Response({'error_description ': 'Censor Board Rating is not provided '}, status=200)

            if 'poster_picture_url' in request.data:
                poster_picture_url = request.data['poster_picture_url']
            else:
                return Response({'error_description ': 'No poster picture was given '}, status=200)

            if 'genre_name' in request.data:
                genre_names = request.data['genre_name']
            else:
                return Response({'error_description ': 'No genres provided for the film '}, status=200)
        except ValueError:
            return Response({'error_description ': 'Invalid Request.Make sure all fields are properly entered '}, status=200)
        if len(name) == 0:
            return Response({'error_description ': 'Name cannot be empty '}, status=200)

        movie_by_name = Movie.objects.filter(name=name).first()  # to check if movie is present

        if movie_by_name:
            return Response({'error_description ': 'Movie already Present in database'}, status=200)

        genre_names = genre_names.split(',')      # to generate list of comma separated string

        genres = []

        for i in genre_names:
            genre_given = Genre.objects.filter(name=i).first()

            if genre_given:
                genres.append(genre_given)

            else:
                return Response({"message": "Invalid Genre ! This genre does not exist make sure you separate genres with ',' "},status=200)

        if duration_in_minutes < 1:
            return Response({"message": "Duration is invalid. A movie cannot be zero or less minutes long"}, status=200)

        if len(genres) < 1:
            return Response({"message": "Invalid. A movie has to have atleast one Genre "}, status=200)

        new_movie_created = Movie.objects.create(name=name, duration_in_minutes=duration_in_minutes,
                            release_date=release_date, censor_board_rating=censor_board_rating,
                            poster_picture_url=poster_picture_url, user=logged_in_user)

        new_movie_created.save()

        for genre in genres:
            MovieGenre.objects.create(movie=new_movie_created, genre=genre)

        return Response(MovieSerializer(instance=new_movie_created).data, status=200)

    return Response({"message": "You are not logged in to perform this action"}, status=400)


@api_view(['GET'])
def get_movie(request):

    movie_id_list = []
    if 'q' in request.query_params:
        name_query = request.query_params['q']

        #  here 'name_icontains' manages full match ,partial match and case sensitive matches

        movies = Movie.objects.filter(name__icontains=name_query)

        if movies:
            for i in range(len(movies)):
                movie_id_list.append(movies[i].id)

        genre_query = name_query

        genre_id = Genre.objects.filter(name__icontains=genre_query).first()

        movie_genre = MovieGenre.objects.filter(genre=genre_id)

        for i in range(len(movie_genre)):
            movie_id_list.append(Movie.objects.filter(id=movie_genre[i].movie_id).first().id)

        my_movie_set = set(movie_id_list)    # To generate a set having only unique values
        movie_id_list = list(my_movie_set)    # converts set back to list

        if len(movie_id_list):

            for i in range(len(movie_id_list)):
                movie_id_list[i] = MovieSerializer(instance=Movie.objects.filter(id=movie_id_list[i]).first()).data

            return Response(movie_id_list, status=200)

        return Response({'message ': 'No such Movies found '}, status=400)

    movies = Movie.objects.all()
    return Response(MovieSerializer(instance=movies,many=True).data, status=200)


# To post a review for a particualar movie
@api_view(['POST'])
def user_review(request):
    logged_in_user = check_token_validity(request)

    # to check if the user is logged in

    if logged_in_user:
        try:

            if 'movie_name' in request.data:
                name = request.data['movie_name']
            else:
                return Response({'error_description ': 'Movie name not provided '}, status=200)

            if 'rating' in request.data:
                user_rating = request.data['rating']
            else:
                return Response({'error_description ': 'Rating is not provided '}, status=200)

            if 'review' in request.data:
                if len(request.data['review']):
                    review = request.data['review']
                else:
                    return Response({'error_description ': 'Review is not provided '}, status=200)

            else:
                return Response({'error_description ': 'Review is not provided '}, status=200)

        except ValueError:

            return Response({'error_description ': 'Invalid Request.Make sure all fields are properly entered '},
                            status=200)

        if len(name) == 0:
            return Response({'error_description ': 'Name cannot be empty '}, status=200)

        movie_id = Movie.objects.filter(name=name).first()

        if movie_id:

            if float(user_rating) >= 5.0:
                return Response({'error_description ': 'Rating should be LESS than 5 '}, status=200)

            previous_rating = Review.objects.filter(user=logged_in_user, movie=movie_id).first()

            if previous_rating:
                return Response({'error_description ': 'You have already reviewed this Movie '}, status=200)

            else:

                new_review_created = Review.objects.create(movie=movie_id, rating= user_rating,
                                                           review=review, user=logged_in_user)
                new_review_created.save()

                average_rating = Review.objects.filter(movie=movie_id).aggregate(avg_rating=Avg('rating'))

                movie_rating_object = Movie.objects.filter(id=movie_id.id).first()
                movie_rating_object.overall_rating = average_rating['avg_rating']
                movie_rating_object.save()

                return Response(ReviewSerializer(instance=new_review_created).data, status=200)

        else:
            return Response({'error_description ': 'No such movie is in our records '}, status=200)
    return Response({'error_description ': 'You are not logged in to perform this action '}, status=200)


@api_view(['GET', 'POST'])
def logout_user(request):
    token_provided = request.META['HTTP_TOKEN']
    valid = AccessToken.objects.filter(access_token=token_provided, is_valid=True).first()

    if valid:

        # sets the is_valid in AccessToken model is set to False(0)

        valid.is_valid=False
        valid.save()
        return Response({'message ': 'You have been successfully Logged-Out '}, status=200)

    return Response({'error_description ': 'User could not be found '}, status=400)
