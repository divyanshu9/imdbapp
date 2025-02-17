from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from imdbapp.models import (
    Movie
)


class MovieSerializer(serializers.ModelSerializer):

    class Meta:
        model = Movie
        exclude = ("id", )