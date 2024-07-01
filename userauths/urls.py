from django.urls import path
from . import views

urlpatterns = [
    path("", views.register, name='register'),
    path("explore/", views.explore, name='explore'),
    path("login/", views.login, name='login'),
    path("logout/", views.logout, name='logout'),
    path('movie/<int:movie_id>/', views.image_detail, name='image_detail'),

    # Search
    path("search/", views.search, name='search'),
    path("auto-search/", views.auto_complete_search, name='auto_complete_search'),

]