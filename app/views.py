from django.shortcuts import render
from static.mock.index import data
# Create your views here.
def index(request):
    
    return render(request, 'index.html', context=data)

def settings(request):
    return render(request, 'settings.html')

def login(request):
    return render(request, 'login.html')

def signup(request):
    return render(request, 'register.html')

def hot(request):
    return render(request, 'index.html')

def ask(request):
    return render(request, 'ask.html')

def question_id(request):
    return render(request, 'question_id.html')

def tag_id(request):
    return render(request, 'tag_bender.html')