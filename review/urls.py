from django.urls import path
from . import views

urlpatterns = [

    path(
        'submitrating/<int:movie_id>/', 
        views.submitrating, 
        name='submitrating'
        ),
    path('user_ratedmovie/', views.user_ratedmovie, name='user_ratedmovie')
]
