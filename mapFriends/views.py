from django.shortcuts import render_to_response, HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages

from mapFriends.facebook import test_token, get_authorization_url,get_token,get_user_data,get_user_friends,get_coordinates
from mapFriends.images import take_image
from mapFriends.forms import LoginForm, RegisterForm
from mapFriends.models import UserProfile



def home(request):
    return render_to_response('index.html', {}, context_instance=RequestContext(request))

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
                    messages.add_message(request, messages.INFO, "Hola %s, te has logueado correctamente" % username)
                    return HttpResponseRedirect("/")
                else:
                    print "[login] Usuario no activo"
                    messages.add_message(request, messages.ERROR, "Usuario no activo")
                    return HttpResponseRedirect("/")
            else:
                print "[login] Usuario o pass incorrecto"
                messages.add_message(request, messages.ERROR, "Usuario o contrasena incorrecta")

    form = LoginForm()
    ctx = {'login' : form}
    print "[login] Enviando formulario de registro"
    return render_to_response('login.html', ctx, context_instance=RequestContext(request))        

def register_view(request):
    form = RegisterForm()

    if request.method == "POST":

        token = request.session['token']
        name = request.session['name']
        register = RegisterForm(request.POST)
        
        if register.is_valid():
            password = register.cleaned_data['password']
        
            try:
                u = User.objects.get(username=name['name'])

                ctx = {'register' : form}
        
                print "[register] Usuario ya existe"
                
                messages.add_message(request, messages.WARNING, "%s ya existe, logueate" %name['name'])

                return HttpResponseRedirect('/login')

            except User.DoesNotExist:
                user = User.objects.create_user(username=name['name'], email=name['email'], password=password)
                facebook_user = UserProfile(user=user, access_token=token['access_token'][0])
                facebook_user.save()
        
                ctx = {}
        
                print "[register] Registrando Usuario"
                messages.add_message(request, messages.INFO, "%s registrado correctamente" %name['name'])
                return render_to_response('index.html', ctx, context_instance=RequestContext(request))
        else:
            
            ctx = {'register' : form}
        
            print "[register] Password no coinciden"
            messages.add_message(request, messages.ERROR, "Passsword no coinciden")
            return render_to_response('register.html', ctx, context_instance=RequestContext(request))

    if 'code' not in request.GET: #Comprobamos si tenemos acceso a sus datos
        url = get_authorization_url(request)
        print "[register] Obteniendo facebook"
        return HttpResponseRedirect(url)

    token = get_token(request)
    name = get_user_data(request, token['access_token'][0])
    request.session['token'] = token
    request.session['name'] = name

    ctx = {'register' : form}
   
    print "[register] Enviando un formuladio de registro"
   
    return render_to_response('register.html', ctx, context_instance=RequestContext(request))

def map(request):
    
    user = User.objects.filter(username=request.user)
    profile = UserProfile.objects.get(user=user)

    token = profile.access_token
    print "Ejecutando"
    url = test_token(request, token)#Test if token is valid
    if url != "":
        print "URL NOT EMPTY"
        return HttpResponseRedirect(url)

    print "[map] Change token"
    profile = UserProfile.objects.get(user=user)
    token = profile.access_token

    data = get_user_data(request, token)

    friends, sites = get_user_friends(request, token)
    location = get_coordinates(request, sites, token)
    friends = take_image(friends)

    ctx = {'data' : data, 'friends' : friends, 'places' : location}
    return render_to_response('map.html', ctx, context_instance=RequestContext(request))

def logout_view(request):
    messages.add_message(request, messages.INFO, "%s , te has deslogueado correctamente" %request.user)
    logout(request)
    print "[logout] Usuario deslogueado"
    
    return HttpResponseRedirect("/")