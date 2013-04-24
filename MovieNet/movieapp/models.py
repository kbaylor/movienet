from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.
class Movie(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=1024)
    year = models.IntegerField(null=True)

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
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=1024)
    awards = models.ManyToManyField(Award, through='ActorNomination')
    movies = models.ManyToManyField(Movie)

class Director(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=1024)
    awards = models.ManyToManyField(Award, through='DirectorNomination')
    movies = models.ManyToManyField(Movie)
    
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
    
class Member(models.Model):
    SEX_CHOICES = (('M', 'Male'), ('F', 'Female'))
    name = models.CharField(max_length=1024)
    sex = models.CharField(max_length=1, choices=SEX_CHOICES)
    email = models.EmailField()
    dob = models.DateField()
    # in reference to rated relationship
    ratings = models.ManyToManyField(Movie, through='Rated')
    
class Rated(models.Model):
    member = models.ForeignKey(Member)
    movie = models.ForeignKey(Movie)
    rating = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(10)])
    class Meta:
        unique_together = ('member', 'movie')
    
    
    
