
from django.shortcuts import render_to_response, HttpResponseRedirect
from django.template import RequestContext
from mapFriends.facebook import * 
from mapFriends.forms import *

def home(request):
    return render_to_response('home.html', {}, context_instance=RequestContext(request))

def login(request):
    
    form = LoginForm()
    ctx = {'login' : form}
    return render_to_response('login.html', ctx, context_instance=RequestContext(request))        

def register(request):
    url = get_authorization_url(request)
    if 'code' not in request.GET: #Comprobamos si tenemos acceso a sus datos
        return HttpResponseRedirect(url)
    else:
        if request.method == "POST":
            register = RegistroForm(request.POST)
            if register.is_valid():

                password = register.cleaned_data['password']
                password_confirm = register.cleaned_data['password_confirm']
                token = get_token(request)
                name = get_user_data(request, token['access_token'][0])
                form = RegistroForm()

                user = User.objects.create_user(username=name['name'], email=name['email'], password=password)
                facebook_user = Facebook(user=user, uid=name['id'], access_token=token['access_token'][0], expire_token= token['expire_token'][0])

                facebook_user.save()

                return render_to_response('/', context_instance= RequestContext(request))
            else:
                ctx = {'register' : form}
                return render_to_response('register.html', ctx, context_instance=RequestContext(request))            
        
        ctx = {'register' : form}
        return render_to_response('register.html', ctx, context_instance=RequestContext(request))

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
    location = []
    
    friends, sites = get_user_friends(request)
    location = get_coordinates(request, sites)
    friends = take_image(friends)

    ctx = {'user' : data, 'friends' : friends, 'places' : location}
    return render_to_response('map.html', ctx, context_instance=RequestContext(request))

def logout(request):
    message = ""
    exit = user_logout(request)
    if exit:
        print "Logout Completed Successfull"
        return HttpResponseRedirect('/')
    else:
        print "Error Logout"

    return render_to_response('home.html', {'men' : message}, context_instance=RequestContext(request))