from django.shortcuts import render
from static.mock.question import questions
from .models import Question
from django.core.paginator import Paginator


# Create your views here.
def index(request):
    page_num = int(request.GET.get('page', 1))
    questions = Question.objects.all().prefetch_related('tags')
    paginator = Paginator(questions, 5)
    page = paginator.page(page_num)
    return render(request, 'index.html', context={"items" : page.object_list, 'page_obj': page})

def settings(request):
    return render(request, 'settings.html',)

def login(request):
    return render(request, 'login.html')

def signup(request):
    return render(request, 'register.html')

def hot(request):
    page_num = int(request.GET.get('page', 1))
    questions = Question.objects.new_questions()
    paginator = Paginator(questions, 5)
    page = paginator.page(page_num)
    return render(request, 'index.html', context={"items": page, 'page_obj': page})

def ask(request):
    return render(request, 'ask.html')

def single_question(request, question_id):
    return render(request, 'single_question.html', context={"item": questions[question_id]})

def tag_id(request, tag):
    page_num = int(request.GET.get('page', 1))
    questions = Question.objects.questions_with_tag(tag)
    paginator = Paginator(questions, 5)
    page = paginator.page(page_num)
    return render(request, 'single_tag.html', context={"items": page, 'page_obj': page, "tag": tag})

def custom_404_view(request, exception):
    return render(request, '404.html', status=404)