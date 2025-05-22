from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy

from app.forms import LoginForm, RegisterForm
# from static.mock.question import questions
from .models import Question
from django.core.paginator import Paginator, EmptyPage
from django.contrib import auth
from django.contrib.auth.decorators import login_required

# Create your views here.

def paginate(objects_list, request, per_page=5):
    paginator = Paginator(objects_list, per_page)
    page_num = request.GET.get('page', 1)
    try:
        page_num = int(page_num) if int(page_num) > 0 else 1
    except (ValueError, TypeError):
        page_num = 1
    try:
        page = paginator.page(page_num)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)
    
    return page

@login_required(login_url=reverse_lazy('login'))
def index(request):
    questions = Question.objects.all_questions()
    page = paginate(questions, request=request)
    return render(request, 'index.html', context={"items" : page, 'page_obj': page})


def settings(request):
    return render(request, 'settings.html',)

def logout(request):
    auth.logout(request)
    return redirect(reverse('login'))

def login(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():    
            user = auth.authenticate(request, **form.cleaned_data)
            if user:
                auth.login(request, user)
                return redirect(reverse_lazy('index'))
            else:
                form.add_error(field=None, error='User not found')
    return render(request, 'login.html', context={'form': form})



def signup(request):
    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():    
            user = auth.authenticate(request, **form.cleaned_data)
            if user:
                form.add_error(field=None, error='User already exists')
            else:
                user = form.save()
                auth.login(request, user)
                return redirect(reverse_lazy('index'))

        
    return render(request, 'register.html', context={'form': form})

def hot(request):
    questions = Question.objects.best_questions()
    page = paginate(questions, request)
    return render(request, 'index.html', context={"items": page, 'page_obj': page})

def ask(request):
    return render(request, 'ask.html')

def single_question(request, question_id):
    question = Question.objects.question_with_id(question_id)
    answers = paginate(question.answers.all(), request)
    return render(request, 'single_question.html', context={"item": question, "answers" :answers, 'page_obj': answers})

def tag_id(request, tag):
    questions = Question.objects.questions_with_tag(tag)
    page = paginate(questions, request)
    return render(request, 'single_tag.html', context={"items": page, 'page_obj': page, "tag": tag})

def custom_404_view(request, exception):
    return render(request, '404.html', status=404)