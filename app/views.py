from django.shortcuts import render
from static.mock.question import questions
from .models import Question
from django.core.paginator import Paginator, EmptyPage


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

def index(request):
    
    questions = Question.objects.all().prefetch_related('tags')
    page = paginate(questions, request=request)
    return render(request, 'index.html', context={"items" : page.object_list, 'page_obj': page})

def settings(request):
    return render(request, 'settings.html',)

def login(request):
    return render(request, 'login.html')

def signup(request):
    return render(request, 'register.html')

def hot(request):
    questions = Question.objects.new_questions()
    page = paginate(questions, request)
    return render(request, 'index.html', context={"items": page, 'page_obj': page})

def ask(request):
    return render(request, 'ask.html')

def single_question(request, question_id):
    return render(request, 'single_question.html', context={"item": questions[question_id]})

def tag_id(request, tag):
    questions = Question.objects.questions_with_tag(tag)
    page = paginate(questions, request)
    return render(request, 'single_tag.html', context={"items": page, 'page_obj': page, "tag": tag})

def custom_404_view(request, exception):
    return render(request, '404.html', status=404)