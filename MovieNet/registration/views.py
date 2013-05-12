from registration.forms import MovienetUserCreationForm
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.core.context_processors import csrf

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