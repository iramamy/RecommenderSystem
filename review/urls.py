from django.urls import path
from . import views

urlpatterns = [

    path(
        'submitrating/<int:movie_id>/', 
        views.submitrating, 
        name='submitrating'
        ),
]