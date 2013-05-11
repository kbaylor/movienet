'''
Created on Apr 29, 2013

@author: Aashish
'''
from django.shortcuts import render_to_response
from MovieNet.etl.imdb import IMDBParser as parser
from movieapp.models import Movie, MovieGenre
from django.contrib.auth.decorators import login_required
from django.core.context_processors import csrf
from movieapp.forms import SearchForm
from django.shortcuts import render, get_object_or_404

from movieapp.models import Director, Movie, Actor, MovieNomination, ActorNomination, DirectorNomination

def index(request):
    return HttpResponse("Hello, world. You're at the movieapp index.")

def movie(request, movieid):
    movie = get_object_or_404(Movie, id=movieid)
    return render(request, 'movie.html', {'movie':movie})

def actor(request, actorid):
    return HttpResponse("You're looking at actor %s." % actorid)

def director(request, did):
    director = get_object_or_404(Director, id=did)
    return render(request, 'director.html', {'director':director})


# def find(request):
#     error = False
#     if 'movie_title' in request.GET:
#         message = 'You searched for: %r' % request.GET['q']
#         movie_title = request.GET['movie_title']
#         if not movie_title:
#             error = True
#         else:
#             movies = Movie.objects.filter(title__icontains=movie_title)
#             return render(request, 'movies_results.html',
#                           {'movies': movies, 'query': movie_title, 'search_type': request.GET['current_choice']})
#     return render(request, 'find_form.html', {'error': error, 'search_types': {'movie','actor','director'}})

def find(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            movie_title = cd['movie_title']
            actor_name = cd['actor_name']
            director_name = cd['director_name']
            start = cd['start_year']
            end = cd['end_year']
            #movie_award = cd['show_movie_oscars']
            #actor_award = cd['show_actor_oscars']
            #director_award = cd['show_director_oscars']
            show_oscars = cd['show_oscars']
            movies = Movie.objects.filter(title__icontains=movie_title)

            if actor_name: 
                actor = Actor.objects.filter(name__icontains=actor_name)           
                movies = movies.filter(actors__in=actor)

            if director_name:
                director = Director.objects.filter(name__icontains=director_name)
                movies = movies.filter(directors__in=director)
            if start and end:
                movies = movies.filter(year__range=(start,end))
            
            #actor.filter(movies__in=movies)
            if show_oscars: 
                movie_oscars = MovieNomination.objects.filter(movie__in=movies)
                actor_oscars = ActorNomination.objects.filter(movie__in=movies)
                director_oscars = DirectorNomination.objects.filter(movie__in=movies)
                return render(request, 'movies_results.html',
                           {'movies': movies, 'query': movie_title, 'show_oscars':show_oscars, 
                                'movie_oscars': movie_oscars, 'actor_oscars':actor_oscars, 'director_oscars':director_oscars})
            else:
                return render(request, 'movies_results.html',
                           {'movies': movies, 'query': movie_title, 'show_oscars':show_oscars})
    else:
        form = SearchForm()
    return render(request, 'find_form.html', {'form': form})
@login_required
def add_movie(request):
    if request.method == 'POST':
        url = request.POST['url']
        movie_info = parser.parse_page(url)
        if movie_info == None:
            pass
        m = Movie.objects.create(title=movie_info['title'], year=movie_info['year'], imdb_rating=movie_info['rating'])
        for genre in movie_info['genres']:
            MovieGenre.objects.create(movie=m.id, genre=genre)
        return render_to_response('movieapp/add_confirmation.html', {'movie_info':movie_info})
    else:
        return render_to_response('movieapp/add.html', csrf(request))
    
    