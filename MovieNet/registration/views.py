from registration.forms import MovienetUserCreationForm
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.core.context_processors import csrf
from movieapp.models import Rated

def register(request):
    if request.method == 'POST': # If the form has been submitted...
        form = MovienetUserCreationForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            form.save()
            return HttpResponseRedirect('/login') # Redirect after POST
    else:
        form = MovienetUserCreationForm() # An unbound form
    c = csrf(request)
    c.update({'form': form, 'login': False})
    return render_to_response('registration/register.html', c)

@login_required
def user_profile(request):
    user = request.user
    rated = Rated.objects.filter(user=user.pk).values('rating', 'movie__title', 'movie__year', 'movie__id')
    return render_to_response('registration/user_profile.html', {'user':user, 'movies_rated':rated})
    #return HttpResponse(movies_rated.values())