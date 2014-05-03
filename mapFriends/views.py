from django.shortcuts import render_to_response
from django.template import RequestContext
from mapFriends.forms import LoginForm, RegistroForm
from django.contrib.auth.models import User   

def index(request):
    return render_to_response('index.html', context_instance = RequestContext(request))

def login(request):
    login = LoginForm()
    ctx = {'login' : login}
    return render_to_response('login.html',ctx, context_instance = RequestContext(request))

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