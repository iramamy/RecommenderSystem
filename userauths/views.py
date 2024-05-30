from django.shortcuts import render, redirect
from django.contrib import auth, messages
from django.core.paginator import Paginator


from .forms import UserRegisterForm
from .models import UserAccount
from review.models import UserReview

import pandas as pd


def explore(request):
    path = 'userauths/data/images.csv'
    data = pd.read_csv(path)

    top_6 = data.sample(6).to_dict('records')
    top_12 = data.sample(200).to_dict('records')

    paginator = Paginator(top_12, 12)
    page = request.GET.get('page')
    image_per_page = paginator.get_page(page)
    

    context = {
        'image_url_6': top_6,
        'images': image_per_page
    }

    return render(request, 'home.html', context)



def image_detail(request, movie_id):
    path = 'userauths/data/images.csv'
    data = pd.read_csv(path)
    image_data = data[data['item_id'] == movie_id].iloc[0]

    top_12 = data.sample(12).to_dict('records')
    top_6 = data.sample(6).to_dict('records')

    try:
        user_review = UserReview.objects.get(
            user__id=request.user.id,
            movieId=movie_id
        )
        user_rating = user_review.rating
        is_exist = True

    except UserReview.DoesNotExist:
        is_exist = False
        user_rating = None

    print("USER RATING IS:", user_rating)

    context = {
        'top_6_images': top_6,
        'top_12_images': top_12,
        'images': image_data,
        'is_exist': is_exist,
        'user_rating': user_rating,
    }

    return render(request, 'details/image_detail.html', context)


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            username = form.cleaned_data['username']

            messages.success(request, "Your account has been created!")
            new_user = auth.authenticate(
                username=form.cleaned_data['email'],
                password=form.cleaned_data['password1']
                )
            auth.login(request, new_user)

            return redirect('explore')
    else:
        form = UserRegisterForm()
    context = {
        'form': form
    }
    return render(request, 'user_accounts/register.html', context)


def login(request):
    if request.user.is_authenticated:
        return redirect('explore')
    
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = auth.authenticate(
            request, 
            email=email, 
            password=password
            )

        if user is not None:
            auth.login(request, user)
            messages.success(request, 'You are logged in!')

            return redirect('explore')
        else:
            messages.error(request, 'Invalid credentials!')

    return render(request, 'user_accounts/login.html')

def logout(request):
    auth.logout(request)
    messages.success(request, 'You are now logged out!')

    return redirect('login')

