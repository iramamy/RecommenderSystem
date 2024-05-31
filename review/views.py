from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import pandas as pd
from .models import UserReview
from .form import ReviewForm


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


def myratedmovie(request):

    rated_movies = UserReview.objects.filter(
        user=request.user
    )

    data = pd.read_csv('./userauths/data/images.csv')
    top_6 = data.sample(6).to_dict('records')
    url_mapping = dict(zip(data['item_id'], data['image']))

    IdWithUrls = []
    for rated_movie in rated_movies:
        movieUrl = url_mapping.get(int(rated_movie.movieId))
        rating = rated_movie.rating
        IdWithUrls.append({
            'movieUrl': movieUrl,
            'rating': rating,
            'movieId': int(rated_movie.movieId),
        })

    context = {
        'IdWithUrls': IdWithUrls,
        'top_6': top_6,
    }

    return render(request, 'details/myratedmovie.html', context)