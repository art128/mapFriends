from django.shortcuts import render_to_response
from django.template import RequestContext
from mapFriends.forms import LoginForm, RegistroForm
from django.contrib.auth.models import User   

from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponseRedirect

def index(request):
    return render_to_response('index.html', context_instance = RequestContext(request))

def login_view(request):
    mensaje = ""
    if request.user.is_authenticated():
        return HttpResponseRedirect('/')
    else:
        if request.method == "POST":
            form = LoginForm(request.POST)
            if form.is_valid():
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']
                usuario = authenticate(username=username, password=password)
                if usuario is not None and usuario.is_active:
                    login(request, usuario)
                    return HttpResponseRedirect('/')
                else:
                    mensaje = 'Usuario y/o password incorrecto'
        form = LoginForm()
        ctx = {'login' : form, 'mensaje' : mensaje}
        return render_to_response('login.html',ctx, context_instance = RequestContext(request))

def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')

def register(request):
    register = RegistroForm()
    if request.method == "POST":
        register = RegistroForm(request.POST)
        if register.is_valid():
            usuario = register.cleaned_data['username']
            email = register.cleaned_data['email']
            password = register.cleaned_data['password']
            password_confirm = register.cleaned_data['password_confirm']

            u = User.objects.create_user(username=usuario, email=email, password=password)
            u.save
            return render_to_response('register_success.html', context_instance= RequestContext(request))
        else:
            ctx = {'register': register}
            return render_to_response('register.html', ctx, context_instance=RequestContext(request))
    ctx = {'register' : register }
    return render_to_response('register.html', ctx, context_instance = RequestContext(request))

def map(request):
    return 