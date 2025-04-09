from django.shortcuts import render
from static.mock.question import questions
from .models import Question
# Create your views here.
def index(request):
    questions = Question.objects.all().prefetch_related('tags')
    return render(request, 'index.html', context={"items" : questions})

def settings(request):
    return render(request, 'settings.html',)

def login(request):
    return render(request, 'login.html')

def signup(request):
    return render(request, 'register.html')

def hot(request):
    questions = Question.objects.new_questions()
    return render(request, 'index.html', context={"items": questions})

def ask(request):
    return render(request, 'ask.html')

def single_question(request, question_id):
    return render(request, 'single_question.html', context={"item": questions[question_id]})

def tag_id(request):
    return render(request, 'tag_bender.html')