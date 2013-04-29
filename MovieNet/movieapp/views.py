from django.http import HttpResponse


def movie(request, movieid):
    return HttpResponse("You're looking at Movie %s." % movieid)

def actor(request, actorid):
    return HttpResponse("You're looking at actor %s." % actorid)

def director(request, did):
    return HttpResponse("You're voting on director %s." % did)