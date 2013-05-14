import json
from registration.forms import MovienetUserCreationForm
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt                                          
from django.core import serializers
from movieapp.models import Rated
from registration.models import MovienetUser

def register(request):
    if request.method == 'POST': # If the form has been submitted...
        form = MovienetUserCreationForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            form.save()
            return HttpResponseRedirect('/login') # Redirect after POST
    else:
        form = MovienetUserCreationForm() # An unbound form
        return render_to_response('registration/register.html', {'form': form, 'login': False}, 
                                  context_instance=RequestContext(request))

@login_required
def user_profile(request):
    user = request.user
    rated = Rated.objects.filter(user=user.pk).values('rating', 'movie__title', 'movie__year', 'movie__id')
    return render_to_response('registration/user_profile.html', {'user':user, 'movies_rated':rated})
   
@login_required
def deactivate(request):
    if request.method == "POST":
        user_instance = MovienetUser.objects.filter(pk=request.user.pk)
        try:
            with open("dropped_user.json") as dropped_users:
                dropped = json.load(dropped_users)
        except IOError:
            dropped = []
        dropped.append(serializers.serialize("json", user_instance, stream=dropped_users))
        with open("dropped_user.json", 'w') as dropped_users:
            json.dump(dropped, dropped_users)
        user_instance.delete()
        return HttpResponseRedirect('/login')
    else:
        return render_to_response("registration/deactivate.html", context_instance=RequestContext(request))
    