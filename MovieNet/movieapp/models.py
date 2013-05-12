from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

from MovieNet import settings
from registration.models import MovienetUser

# Create your models here.
class Movie(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=1024)
    year = models.IntegerField(null=True)
    imdb_rating = models.DecimalField(null=True, max_digits=2, decimal_places=1)
    ratings = models.ManyToManyField(MovienetUser, through='Rated')

class MovieGenre(models.Model):
    movie = models.ForeignKey(Movie)
    genre = models.CharField(max_length=1024)

class Award(models.Model):
    name = models.CharField(max_length=255)
    year = models.IntegerField()
    actorAwards = models.ManyToManyField(Movie, through='ActorNomination', related_name='actor_award_set')
    directorAwards = models.ManyToManyField(Movie, through='DirectorNomination', related_name='director_award_set')
    class Meta:
        unique_together = ('name', 'year')
    
class Actor(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=1024)
    awards = models.ManyToManyField(Award, through='ActorNomination')
    movies = models.ManyToManyField(Movie, related_name = 'actors')

class Director(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=1024)
    awards = models.ManyToManyField(Award, through='DirectorNomination')
    movies = models.ManyToManyField(Movie, related_name = 'directors')
    
class MovieNomination(models.Model):
    movie = models.ForeignKey(Movie)
    award = models.ForeignKey(Award)
    won = models.BooleanField()
    class Meta:
        unique_together = ('movie', 'award')
    
class ActorNomination(models.Model):
    movie = models.ForeignKey(Movie)
    actor = models.ForeignKey(Actor)
    award = models.ForeignKey(Award)
    won = models.BooleanField()
    class Meta:
        unique_together = ('movie', 'actor', 'award')
    
class DirectorNomination(models.Model):
    movie = models.ForeignKey(Movie)
    director = models.ForeignKey(Director)
    award = models.ForeignKey(Award)
    won = models.BooleanField()
    class Meta:
        unique_together = ('movie', 'director', 'award')
    
class Rated(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    movie = models.ForeignKey(Movie)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])
    date_rated = models.DateTimeField()
    class Meta:
        unique_together = ('user', 'movie')
    
    
    
