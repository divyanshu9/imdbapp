from django.urls import path

from . import views


urlpatterns = [
    path(r'movie/',
             views.MovieListLookupAPIView.as_view()),
    path(r'movie/<str:title>/',
         views.MovieListLookupAPIView.as_view()),
]
