from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
import pickle
from django.contrib import messages
import pandas as pd
from .models import UserReview
from .form import ReviewForm

from rec_model.get_movie_id import recommend_movies_for_user


# Load the save matrices
with open('./rec_model/movie_matrix.pkl', 'rb') as f:
    movie_matrix = pickle.load(f)

with open('./rec_model/movie_bias.pkl', 'rb') as f:
    movie_bias = pickle.load(f)


@login_required(login_url='login')
def submitrating(request, movie_id):
    url = request.META.get("HTTP_REFERER")

    if request.method == "POST":
        try:
            rating = UserReview.objects.get(
                user__id=request.user.id,
                movieId=movie_id
            )

            form = ReviewForm(request.POST, instance=rating)
            form.save()
            messages.success(request, "Rating updated!")

            return redirect(url)
        
        except UserReview.DoesNotExist:

            form = ReviewForm(request.POST)

            if form.is_valid():
                data = UserReview()
                data.user_id = request.user.id
                data.rating = form.cleaned_data['rating']
                data.movieId = movie_id
                data.ip = request.META.get("REMOTE_ADDR")
                data.save()

                messages.success(request, "Rating submitted!")

                return redirect(url)


@login_required(login_url='login')
def user_ratedmovie(request):

    rated_movies = UserReview.objects.filter(
        user=request.user
    )

    user_movie_ids = []
    for review in rated_movies:
        user_movie_ids.append(int(review.movieId))

    get_recommendation_id = recommend_movies_for_user(
        user_movie_ids,
        movie_matrix,
        movie_bias
    )

    print('User movide id watched', user_movie_ids)
    print('User movide id recommended', get_recommendation_id)

    path = 'userauths/data/movies.dat'
    column_names = ['item_id', 'title', 'genres']

    data = pd.read_csv(
        path,
        sep='::',
        engine='python',
        header=None,
        names=column_names,
        encoding='latin1'
        )

    data['genres'] = data['genres'].str.replace('|', ', ')

    top_12 = data[data['item_id'].isin(get_recommendation_id)].to_dict('records')

    genre_mapping = dict(zip(data['item_id'], data['genres']))

    IdWithGenres = []
    for rated_movie in rated_movies:
        movieGenre = genre_mapping.get(int(rated_movie.movieId))
        rating = rated_movie.rating
        IdWithGenres.append({
            'genres': movieGenre,
            'rating': rating,
            'movieId': int(rated_movie.movieId),
        })

    context = {
        'IdWithGenres': IdWithGenres,
        'top_12': top_12,
    }

    return render(request, 'details/user_ratedmovie.html', context)
