'''
Created on Apr 29, 2013

@author: Aashish
'''
from django.http import HttpResponse
from django.db.models import Count

from movieapp.forms import SearchForm, BasicSearchForm
from django.shortcuts import render_to_response
from MovieNet.etl.imdb import IMDBParser as parser
from movieapp.models import Movie, MovieGenre
from django.contrib.auth.decorators import login_required
from django.core.context_processors import csrf
from django.shortcuts import render, get_object_or_404

from movieapp.models import Director, Movie, Actor, MovieNomination, ActorNomination, DirectorNomination, Rated

  
@login_required
def add_movie(request):
    if request.method == 'POST':
        url = request.POST['url']
        movie_info = parser.parse_page(url)
        if movie_info == None:
            pass
        name = movie_info['title']
        year = movie_info['year']
        rating = movie_info['rating']
        genres = movie_info['genres']
        regex = name + '($|([ ]*\\(.+\\)$))'
        movies_in_db = Movie.objects.filter(title__iregex=regex, year__exact=year)
        if not movies_in_db:
            movies_in_db = [Movie.objects.create(title=name, year=year, imdb_rating=rating)]
        movies_in_db.update(imdb_rating=rating)
        movie_info['titles'] = movies_in_db
        for movie in movies_in_db:
            pk = movie.pk
            #return HttpResponse(pk)
            movie_db_genres = [a.genre for a in MovieGenre.objects.filter(pk=pk)]
            for genre in genres:
                if genre not in movie_db_genres:
                    MovieGenre.objects.create(movie_id=pk, genre=genre)
            for actor in movie_info['actors']:
                actors = Actor.objects.filter(name=actor)
                if not actors:
                    actors = [Actor.objects.create(name=actor)]
                for actor_instance in actors:
                    if movie not in actor_instance.movies.values_list('title', flat=True):
                        actor_instance.movies.add(movie)
                        actor_instance.save()
            for director in movie_info['directors']:
                directors = Director.objects.filter(name=director)
                if not directors:
                    directors = [Director.objects.create(name=director)]
                for director_instance in directors:
                    if movie not in director_instance.movies.values_list('title', flat=True):
                        director_instance.movies.add(movie)
                        director_instance.save()         
        return render_to_response('movieapp/add_confirmation.html', {'movie_info':movie_info})
    else:
        return render_to_response('movieapp/add.html', csrf(request))
    
@login_required
def movie(request, movieid):
    movie = get_object_or_404(Movie, id=movieid)
    try:
        rating = Rated.objects.get(movie=movieid, user=request.user.pk)
    except Rated.DoesNotExist:
        rating = None
    return render(request, 'movieapp/movie.html', {'movie':movie, 'rating':rating})

@login_required
def actor(request, actorid):
    actor = get_object_or_404(Actor, id=actorid)
    costars_id = Movie.objects.filter(pk__in=actor.movies.all).values('actors')
    costars_id = costars_id.annotate(num_movies=Count('actors')).order_by('-num_movies')[1:6]
    print costars_id
    #id_values = costars_id.values_list('actors', flat=True)
    # id_values = [a.actors for a in costars_id]
    
    #ids = []
    costar_list = []
    for actor_dict in costars_id:
        #ids.append(actor_dict['actors'])
        costar_list.append([Actor.objects.get(id=actor_dict['actors']), actor_dict['num_movies']])
    #return HttpResponse(costars_id)
    #costars = Actor.objects.filter(id__in=ids)
    return render(request, 'movieapp/actor.html', {'actor':actor, 'costars':costar_list});

@login_required
def director(request, did):
    director = get_object_or_404(Director, id=did)
    return render(request, 'movieapp/director.html', {'director':director})


@login_required
def find(request):
    if request.method == 'POST':
        form = BasicSearchForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            text = cd['query']
            search_type = cd['search_type']
            
            if search_type=='movie':
                return_set = Movie.objects.filter(title__icontains=text)
                

            if search_type=='actor': 
                return_set = Actor.objects.filter(name__icontains=text)

            if search_type=='director':
                return_set = Director.objects.filter(name__icontains=text)
            return render(request, 'movieapp/basic_search_results.html',
                           {'return_set': return_set, 'query': text, 'search_type':search_type})
    else:
        form = BasicSearchForm()
    return render(request, 'movieapp/find_form.html', {'form': form})


def advancedfind(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            movie_title = cd['movie_title']
            actor_name = cd['actor_name']
            director_name = cd['director_name']
            start = cd['start_year']
            end = cd['end_year']
            ratings_start = cd['min_rating']
            ratings_end = cd['max_rating']
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
           
                
           ## ratings=Rated.objects.filter(movie__in=movies).annotate(avg_rating=Avg('rating'))
            #ratings.annotate(Avg('rating'))
            
           ## if rating_start and rating_end:
           ##     ratings = ratings.filter(avg_rating__range=(rating_start,rating_end))
           ##     movies = movies.filter(pk__in=ratings)
            if show_oscars: 
                movie_oscars = MovieNomination.objects.filter(movie__in=movies)
                actor_oscars = ActorNomination.objects.filter(movie__in=movies)
                director_oscars = DirectorNomination.objects.filter(movie__in=movies)
                return render(request, 'movieapp/advanced_search_results.html',
                           {'movies': movies, 'query': movie_title, 'show_oscars':show_oscars, 
                                'movie_oscars': movie_oscars, 'actor_oscars':actor_oscars, 'director_oscars':director_oscars})
            else:
                return render(request, 'movieapp/advanced_search_results.html',
                           {'movies': movies, 'query': movie_title, 'show_oscars':show_oscars})
    else:
        form = SearchForm()
    return render(request, 'movieapp/find_form.html', {'form': form})