from django.shortcuts import render

def index(request):
    return render(request, 'index.html')

def member(request):
    return render(request, 'map.html')