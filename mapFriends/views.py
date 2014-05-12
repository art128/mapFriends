from django.shortcuts import render_to_response, HttpResponseRedirect
from django.template import RequestContext
from mapFriends.facebook import * 


def home(request):
    return render_to_response('home.html', {}, context_instance=RequestContext(request))

def login(request):
    url = get_authorization_url(request)
    return HttpResponseRedirect(url)

def auth(request):
    mensage = ''
    if verify(request):
        mensage = 'Login Correcto'
        get_token(request)
    else:
        mensage = 'Login Incorrecto'

    ctx = {'men' : mensage}

    return render_to_response('home.html', ctx, context_instance=RequestContext(request))        

def map(request):
    friends = []
    sites = []
    #location = []

    data = get_user_data(request)
    friends, sites = get_user_friends(request)
    #location = get_coordinates(request, sites)
    #take_image(friends)
    ctx = {'user' : data, 'friends' : friends}
    return render_to_response('map.html', ctx, context_instance=RequestContext(request))

def logout(request):
    user_logout(request)
    return render_to_response('home.html', {}, context_instance=RequestContext(request))