from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
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
            messages.success(request, "Review updated!")

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

                messages.success(request, "Review submitted!")

                return redirect(url)
