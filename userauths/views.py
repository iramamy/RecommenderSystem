from django.shortcuts import render, redirect, HttpResponse
from django.contrib import auth, messages
from django.core.paginator import Paginator
from django.http import JsonResponse

from .forms import UserRegisterForm
from .models import UserAccount
from review.models import UserReview

import pandas as pd


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

def explore(request):

    top_6 = data.sample(6).to_dict('records')
    all_movies = data.to_dict('records')

    paginator = Paginator(all_movies, 12)
    page = request.GET.get('page')
    image_per_page = paginator.get_page(page)
    
    context = {
        'new_top_6': top_6,
        'images': image_per_page,
        'all_movies': all_movies
    }

    return render(request, 'home.html', context)


def image_detail(request, movie_id):
    
    image_data = data[data['item_id'] == movie_id].iloc[0]

    get_genres = data[data['item_id']==movie_id]['genres'].values[0]
    
    keywords = get_genres.split(',')
    keywords = '|'.join(keywords)
    
    might_like_data = data[data['genres'].str.contains(keywords, regex=True)]
    different_data = data[~data['genres'].str.contains(keywords, regex=True)]

    top_12 = might_like_data.sample(12).to_dict('records')
    top_6 = different_data.sample(6).to_dict('records')

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

def search(request):
    if "keyword" in request.GET:
        keyword = request.GET.get('keyword', '').strip()

        if keyword:
            top_6 = data.sample(6).to_dict('records')
            df_filtered = data[data['title'].str.contains(keyword, case=False, regex=False)]
            all_movies = df_filtered.to_dict('records')

            paginator = Paginator(all_movies, 12)
            page = request.GET.get('page')
            image_per_page = paginator.get_page(page)
            
            context = {
                'all_movies': image_per_page,
                'keyword': keyword,
                'top_6': top_6
            }

            return render(request, 'details/search_result.html', context)
        
    return render(request, 'details/search_result.html', {}) 

def auto_complete_search(request):
    keyword = request.GET.get("keyword", "").strip()
    df = data[data['title'].str.contains(keyword, case=False, regex=False)]

    json_data = df['title'].to_list()
    
    context = {
        'status': 200,
        'data': json_data
    }

    return JsonResponse(context)
