from django.db import models

class Movie(models.Model):
    title = models.CharField(max_length=255)
    release_year = models.IntegerField()
    imdb_rating = models.DecimalField(max_digits=3, decimal_places=1, null=True)
    director = models.CharField(max_length=255, null=True, blank=True)
    cast = models.TextField(null=True, blank=True)
    plot_summary = models.TextField(null=True, blank=True)
    genre = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.title