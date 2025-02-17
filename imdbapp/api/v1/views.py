import json

from rest_framework.views import APIView
from rest_framework import generics
from .serializers import (
    MovieSerializer
)

from imdbapp.models import (
    Movie
)

class MovieListLookupAPIView(generics.ListAPIView):
    """
    Movie List Lookup API that filters movies by title if provided,
    otherwise returns all movies.
    """
    serializer_class = MovieSerializer

    def get_queryset(self):
        """
        Optionally restricts the queryset based on the title in the URL.
        If no title is provided, returns all movies.
        """
        title = self.kwargs.get('title', None)  # Get 'title' from URL, if exists
        if title:
            # If a title is provided, filter movies by the title
            queryset = Movie.objects.filter(title__icontains=title)  # Case-insensitive search by title
        else:
            # If no title is provided, return all movies
            queryset = Movie.objects.all()
        return queryset
