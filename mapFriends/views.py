
from django.shortcuts import render_to_response, HttpResponseRedirect
from django.template import RequestContext
from mapFriends.facebook import * 
from mapFriends.forms import *
from mapFriends.models import *

def home(request):
    return render_to_response('home.html', {}, context_instance=RequestContext(request))

def login(request):
    
    if request.method == "POST":
        login = LoginForm(request.POST)
        if login.is_valid():
            print login.cleaned_data['username']
            try:
                user = User.objects.get(username=login.cleaned_data['username'])
                #Implementar el login correctamente
                #Comprobar la contraseña
                #Guardar contraseña es correcto??
                #Comprobar el accestoken, implemtarlo
            except User.DoesNotExist:
                print "NO EXISTE"

    form = LoginForm()
    ctx = {'login' : form}
    return render_to_response('login.html', ctx, context_instance=RequestContext(request))        

def register(request):
    print "ENTRANDO EN REGISRO"
    if request.method == "POST":
        print "REGISTRANDO UN USUARIO"
        token = request.session['token']
        name = request.session['name']
        register = RegistroForm(request.POST)
        password = register['password']

        try:
            u = User.objects.get(username=name['name'])
        except User.DoesNotExist:
            user = User.objects.create_user(username=name['name'], email=name['email'], password=password)
            facebook_user = UserProfile(user=user, access_token=token['access_token'][0])
            facebook_user.save()
            ctx = {'msg' : 'OK'}
            return render_to_response('home.html', ctx, context_instance=RequestContext(request))
        ctx = {'msg' : 'ERROR'}
        print "ERROR USUARIO EXISTE"
        return HttpResponseRedirect('/')

    if 'code' not in request.GET: #Comprobamos si tenemos acceso a sus datos
        url = get_authorization_url(request)
        
        return HttpResponseRedirect(url)
    print "NO HE REGISTRADO NADA"
    token = get_token(request)
    name = get_user_data(request, token['access_token'][0])
    request.session['token'] = token
    request.session['name'] = name
    form = RegistroForm()
    ctx = {'register' : form}

    return render_to_response('register.html', ctx, context_instance=RequestContext(request))

def auth(request):
    mensage = ''
    if verify(request):
        mensage = 'Login Correcto'
        get_token(request)
    else:
        mensage = 'Login Incorrecto'

    ctx = {'msg' : mensage}

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

    return render_to_response('home.html', {'msg' : message}, context_instance=RequestContext(request))