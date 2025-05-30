from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy

from app.forms import AnswerForm, AskForm, LoginForm, RegisterForm, SettingsForm
# from static.mock.question import questions
from .models import Answer, AnswerLike, Avatar, Question, Profile, QuestionLike, Tag
from django.core.paginator import Paginator, EmptyPage
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

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
    questions = Question.objects.all_questions(user=request.user)
    page = paginate(questions, request=request)
    return render(request, 'index.html', context={"items" : page, 'page_obj': page})

@login_required
def settings(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        form = SettingsForm(request.POST, request.FILES)
        if form.is_valid():
            
            request.user.email = form.cleaned_data['email']
            request.user.save()
            
            profile.nickname = form.cleaned_data['nickname']
            if form.cleaned_data['avatar']:
                avatar = Avatar(image=form.cleaned_data['avatar'])
                avatar.save()
                profile.avatar = avatar
            profile.save()
            
            return redirect('settings')
    else:
    
        initial_data = {
            'email': request.user.email,
            'nickname': profile.nickname
        }
        form = SettingsForm(initial=initial_data)
    
    return render(request, 'settings.html', context={"item": profile, 'form': form})

@login_required
def logout(request):
    auth.logout(request)
    next_page = request.GET.get('continue', 'login')
    return redirect(next_page)

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
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():    
            user = auth.authenticate(request, **form.cleaned_data)
            if user:
                form.add_error(field=None, error='User already exists')
            else:
                user = form.save()
                auth.login(request, user)
                return redirect(reverse_lazy('index'))

        
    return render(request, 'register.html', context={'form': form})

@login_required
def hot(request):
    questions = Question.objects.best_questions(user=request.user)
    page = paginate(questions, request)
    return render(request, 'index.html', context={"items": page, 'page_obj': page})

@login_required
def ask(request):
    form = AskForm()
    if request.method == 'POST':
        form = AskForm(request.POST)
        if form.is_valid():
            question = form.save(user=request.user)
            return redirect(reverse_lazy('question', kwargs={'question_id': question.id}))
    return render(request, 'ask.html', {'form': form})

@login_required
def single_question(request, question_id):
    question = Question.objects.question_with_id(question_id)
    # print(Answer.objects.all_with_avatars(question=question, user=request.user).count())
    answers = paginate(Answer.objects.all_with_avatars(question=question, user=request.user), request)
    avatar = Profile.objects.get_avatar_url(user=question.author)
    isLiked = QuestionLike.objects.filter(question=question, user=request.user).exists()
    form = AnswerForm()
    print(answers[0].blockBecauseNotCorrect)
    print(answers[1].blockBecauseNotCorrect)
    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            form.save(user=request.user, question_id=question_id)
            return redirect(reverse_lazy('question', kwargs={'question_id': question.id}))
    return render(request, 'single_question.html', context={"item": question, "answers" :answers, 'page_obj': answers, 'form': form, 'isLiked': isLiked, 'likes_count': question.likes.count(), 'avatar': avatar, 'hasCheckBtn': request.user.id != question.author.id})

def tag_id(request, tag):
    questions = Question.objects.questions_with_tag(tag)
    page = paginate(questions, request)
    return render(request, 'single_tag.html', context={"items": page, 'page_obj': page, "tag": tag})

def custom_404_view(request, exception):
    return render(request, '404.html', status=404)

@login_required
@require_POST
def likeQuestion(request, question_id):
    question = Question.objects.question_with_id(question_id)
    if question:
        questionLike, is_created = QuestionLike.objects.get_or_create(user=request.user, question=question) 
        if not is_created:
            questionLike.delete()
    return JsonResponse({'likes_count': QuestionLike.objects.filter(question=question).count(), 'isLiked': is_created})



@login_required
@require_POST
def likeAnswer(request, answer_id):
    answer = Answer.objects.get(id=answer_id)
    if answer:
        answerLike, is_created = AnswerLike.objects.get_or_create(user=request.user, answer=answer) 
        if not is_created:
            answerLike.delete()
    return JsonResponse({'likes_count': AnswerLike.objects.filter(answer=answer).count(), 'isLiked': is_created})

@login_required
@require_POST
def correctAnswer(request, answer_id):
    try:
        # Получаем ответ и связанный вопрос
        answer = get_object_or_404(Answer, id=answer_id)
        question = answer.question
        
        # Проверяем, что текущий пользователь - автор вопроса
        if question.author != request.user:
            return JsonResponse({'error': 'You are not the author of this question'}, status=403)
        
        # Если ответ уже является правильным - снимаем отметку
        if question.correct_answer == answer:
            question.correct_answer = None
            is_checked = False
        else:
            # Если у вопроса уже есть другой правильный ответ - запрещаем изменение
            if question.correct_answer is not None:
                return JsonResponse({
                    'error': 'This question already has a correct answer',
                    'isChecked': False
                }, status=400)
            
            # Устанавливаем новый правильный ответ
            question.correct_answer = answer
            is_checked = True
            
        question.save()
        
        return JsonResponse({'isChecked': is_checked})
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)
    

def tag_questions(request, tag_title):
    tag = get_object_or_404(Tag, title=tag_title)
    questions = Question.objects.filter(tags=tag).order_by('-created_at')
    return render(request, 'questions/tag_questions.html', {
        'tag': tag,
        'questions': questions
    })