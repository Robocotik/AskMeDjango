from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'index.html')

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