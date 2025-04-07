from django.shortcuts import render
from static.mock.question import questions
# Create your views here.
def index(request):
    
    return render(request, 'index.html', context={"items" : questions})

def settings(request):
    return render(request, 'settings.html',)

def login(request):
    return render(request, 'login.html')

def signup(request):
    return render(request, 'register.html')

def hot(request):
    return render(request, 'index.html')

def ask(request):
    return render(request, 'ask.html')

def single_question(request, question_id):
    return render(request, 'single_question.html', context={"item": questions[question_id]})

def tag_id(request):
    return render(request, 'tag_bender.html')