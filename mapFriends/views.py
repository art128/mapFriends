
from django.shortcuts import render_to_response, HttpResponseRedirect
from django.template import RequestContext
from mapFriends.facebook import * 
from mapFriends.forms import *
from mapFriends.models import *
from django.contrib.auth import authenticate, login, logout

def home(request):
    return render_to_response('home.html', {}, context_instance=RequestContext(request))

def login_view(request):
    
    if request.method == "POST":
        login_form = LoginForm(request.POST)
        if login_form.is_valid():

            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    print "[login] Usuario valido"
                    login(request, user)
                    return HttpResponseRedirect("/")
                else:
                    print "[login] Usuario no activo"
                    return HttpResponseRedirect("/")
            else:
                print "[login] Usuario o pass incorrecto"
            

    form = LoginForm()
    ctx = {'login' : form}
    print "[login] Enviando formulario de registro"
    return render_to_response('login.html', ctx, context_instance=RequestContext(request))        

def register(request):
    if request.method == "POST":
        token = request.session['token']
        name = request.session['name']
        register = RegistroForm(request.POST)
        if register.is_valid():
            password = register.cleaned_data['password']
            try:
                u = User.objects.get(username=name['name'])
            except User.DoesNotExist:
                user = User.objects.create_user(username=name['name'], email=name['email'], password=password)
                facebook_user = UserProfile(user=user, access_token=token['access_token'][0], expired_token=token['expires'][0])
                facebook_user.save()
                ctx = {'msg' : 'OK'}
                print "[register] Registrando Usuario"
                return render_to_response('home.html', ctx, context_instance=RequestContext(request))

            ctx = {'msg' : 'ERROR'}
            print "[register] Usuario ya existe"
            return HttpResponseRedirect('/')

    if 'code' not in request.GET: #Comprobamos si tenemos acceso a sus datos
        url = get_authorization_url(request)
        print "[register] Obteniendo facebook"
        return HttpResponseRedirect(url)

    token = get_token(request)
    name = get_user_data(request, token['access_token'][0])
    request.session['token'] = token
    request.session['name'] = name
    form = RegistroForm()
    ctx = {'register' : form}
    print "[register] Enviando un formuladio de registro"
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

def logout_view(request):
    logout(request)

    return HttpResponseRedirect("/")