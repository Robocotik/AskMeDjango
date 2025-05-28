from django.db import models
from django.contrib.auth.models import User
from django.db.models import Manager
from django.db.models import Count
from django.db.models import Prefetch
from django.core.exceptions import ObjectDoesNotExist

from askme_startkin import settings
from askme_startkin.settings import MEDIA_URL
from django.db.models import Case, When, Value, CharField, F
from django.db.models.functions import Concat

from django.utils import timezone
from django.core.cache import cache
from datetime import timedelta
from django.db.models import Q
from django.contrib.auth.models import BaseUserManager


class Avatar(models.Model):
    image = models.ImageField(upload_to='uploads/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def image_url(self):
        if self.image:
            return self.image.url
        return f"{settings.STATIC_URL}{settings.DEFAULT_AVATAR_URL}"

class ProfileManager(Manager):
    def profile_with_id(self, id):
        try:
            return Profile.objects.get(id=int(id))

        except ObjectDoesNotExist:
            return None
    
    def get_avatar_url(self, user):
        try:
            profile = Profile.objects.get(user=user)
            if profile.avatar:
                return profile.avatar.image_url  # Используем новый метод
        except (AttributeError, Profile.DoesNotExist):
            pass
        return f"/{settings.STATIC_URL}{settings.DEFAULT_AVATAR_URL}"
        
class Profile(models.Model):
    objects = ProfileManager()
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.OneToOneField(Avatar, on_delete=models.PROTECT, null=True, blank=True)
    nickname = models.CharField(max_length=255, null=True, blank=True)
    
    
    def __str__(self) -> str:
        return self.user.username



class QuestionManager(Manager):
    
    def all_questions(self, user=None):
        queryset = self.select_related(
            'author__profile__avatar'
        ).annotate(
            answer_count=Count('answers', distinct=True),
            likes_count=Count('likes', distinct=True),
            avatar_url=Case(
                When(
                    author__profile__avatar__isnull=False,
                    then=Concat(
                        Value('/' + MEDIA_URL),
                        F('author__profile__avatar__image'),
                        output_field=CharField()
                    )
                ),
                default=Value('/static/empty_avatar.jpg'),
                output_field=CharField()
            )
        )
        
        if user and user.is_authenticated:
            # Добавляем подзапрос для проверки лайка
            liked_questions = QuestionLike.objects.filter(
                question=models.OuterRef('pk'),
                user=user
            ).values('question')[:1]
            
            queryset = queryset.annotate(
                isLiked=Case(
                    When(
                        id__in=liked_questions,
                        then=Value(True)
                    ),
                    default=Value(False),
                    output_field=models.BooleanField()
                )
            )
        else:
            queryset = queryset.annotate(
                isLiked=Value(False, output_field=models.BooleanField())
            )
        
        return queryset.prefetch_related('tags').distinct()
    
    def new_questions(self, user=None):
        return self.prefetch_related(
            'tags',
            'likes'
        ).select_related(
            'author__profile__avatar'
        ).annotate(
            answer_count=Count('answers', distinct=True),
            likes_count=Count('likes', distinct=True),
            avatar_url=Case(
                When(
                    author__profile__avatar__isnull=False,
                    then=Concat(
                        Value('/' + MEDIA_URL),
                        F('author__profile__avatar__image'),
                        output_field=CharField()
                    )
                ),
                default=Value('/static/empty_avatar.jpg'),
                output_field=CharField()
            ),
                isLiked=Case(
                    When(
                        likes__user=user,  # Исправлено здесь
                        then=Value(True)
                    ),
                    default=Value(False),
                    output_field=models.BooleanField()
                )
        ).distinct().order_by('-created_at')
    
    def best_questions(self, user=None):
    # Сначала получаем базовый queryset с аннотацией likes_count
        queryset = self.prefetch_related(
            'tags'
        ).select_related(
            'author__profile__avatar'
        ).annotate(
            answer_count=Count('answers', distinct=True),
            likes_count=Count('likes', distinct=True),
            avatar_url=Case(
                When(
                    author__profile__avatar__isnull=False,
                    then=Concat(
                        Value('/' + MEDIA_URL),
                        F('author__profile__avatar__image'),
                        output_field=CharField()
                    )
                ),
                default=Value('/static/empty_avatar.jpg'),
                output_field=CharField()
            )
        ).order_by('-likes_count')
        
        # Затем добавляем проверку лайка отдельно, если пользователь аутентифицирован
        if user and user.is_authenticated:
            liked_questions = QuestionLike.objects.filter(
                question=models.OuterRef('pk'),
                user=user
            ).values('question')[:1]
            
            queryset = queryset.annotate(
                isLiked=Case(
                    When(
                        id__in=liked_questions,
                        then=Value(True)
                    ),
                    default=Value(False),
                    output_field=models.BooleanField()
                )
            )
        else:
            queryset = queryset.annotate(
                isLiked=Value(False, output_field=models.BooleanField())
            )
        
        return queryset.distinct()
    
    def question_with_id(self, id):
        try:
            return self.prefetch_related(
                Prefetch('answers', queryset=Answer.objects.annotate(likes_count=Count('answer_likes'))),
                'tags',
                'likes'
            ).annotate(
                answer_count=Count('answers')
            ).get(id=int(id))
        except ObjectDoesNotExist:
            return None
    
    
        
    def questions_with_tag(self, tag_title):
        self = self.select_related(
            'author__profile__avatar'
            ).annotate(answer_count=Count('answers'), likes_count=Count('likes'), avatar_url=Case(
                When(
                    author__profile__avatar__isnull=False,
                    then=Concat(
                        Value('/' + MEDIA_URL),
                        F('author__profile__avatar__image'),
                        output_field=CharField()
                    )
                ),
                default=Value('/static/empty_avatar.jpg'),
                output_field=CharField()
            ))
        try:
            tag = Tag.objects.get(title=tag_title)
        except Tag.DoesNotExist:
            return self.none()
        
        return self.filter(tags=tag).distinct()
    

    
class Question(models.Model):
    id = models.BigAutoField(primary_key=True, editable=False)
    correct_answer = models.ForeignKey(
        'Answer', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='correct_for_questions'
    )
    objects = QuestionManager()
    title = models.CharField(max_length=1000, default='title_placeholder')
    desc  = models.CharField(max_length=20000, default='desc_placeholder') 
    author = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    tags = models.ManyToManyField('Tag', related_name='questions')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self) -> str:
        return self.title

class TagManager(models.Manager):
    def popular_tags(self):
        cache_key = 'popular_tags'
        tags = cache.get(cache_key)
        if tags is None:
            three_months_ago = timezone.now() - timedelta(minutes=1)
            tags = self.annotate(
                num_questions=Count('questions', filter=Q(questions__created_at__gte=three_months_ago))).order_by('-num_questions')[:10]
            cache.set(cache_key, tags, 60) 
        return tags

class Tag(models.Model):
    title = models.CharField(max_length=255)
    objects = TagManager() 
    
    def __str__(self) -> str:
        return self.title
    

class AnswerManager(Manager):
    def all_with_avatars(self, question, user=None):

        return self.filter(question=question).select_related(
            'author__profile__avatar'
        ).annotate(
            likes_count=Count('answer_likes'),
            avatar_url=Case(
                When(
                    author__profile__avatar__isnull=False,
                    then=Concat(
                        Value('/' + MEDIA_URL),
                        F('author__profile__avatar__image'),
                        output_field=CharField()
                    )
                ),
                default=Value('/static/empty_avatar.jpg'),
                output_field=CharField()
            ),
            isLiked=Case(
                    When(
                        answer_likes__user=user,
                        then=Value(True)
                    ),
                    default=Value(False),
                    output_field=models.BooleanField()
                ),
            isDisabled=Case(
                When(
                    question__author__id=user.id,
                    then=Value(False)
                ),
                default=Value(True),
                output_field=models.BooleanField()
            ),
            isChecked=Case(
                When(
                    id=F('question__correct_answer__id'),  # Исправлено здесь
                    then=Value(True)
                ),
                default=Value(False),
                output_field=models.BooleanField()
            ),
            blockBecauseNotCorrect=Case(
                When(question__correct_answer__isnull=True, then=Value(False)),
                When(id=F('question__correct_answer__id'), then=Value(False)),
                default=Value(True),
                output_field=models.BooleanField()
            )
        )
    
class Answer(models.Model):
    objects = AnswerManager()
    question = models.ForeignKey('Question', on_delete=models.CASCADE, related_name='answers', blank=True, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    content = models.CharField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.question
    
class QuestionLike(models.Model):
    question = models.ForeignKey('Question',default=None, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(User, default=None, on_delete=models.CASCADE)
    class Meta:
        unique_together = ('question', 'user')
class AnswerLike(models.Model):
    answer = models.ForeignKey('Answer',default=None, on_delete=models.CASCADE, related_name='answer_likes')
    user = models.ForeignKey(User, default=None, on_delete=models.CASCADE)
    class Meta:
        unique_together = ('answer', 'user')




class UserQuerySet(models.QuerySet):
    def top_users(self):
        cache_key = 'top_users'
        users = cache.get(cache_key)
        if users is None:
            one_week_ago = timezone.now() - timedelta(minutes=1)
            
            users_dict = {}
            
            for user in self.annotate(
                question_score=Count('question__likes', filter=Q(question__created_at__gte=one_week_ago))
            ).order_by('-question_score')[:10]:
                users_dict[user.id] = {
                    'user': user,
                    'total_score': getattr(user, 'question_score', 0),
                    'question_score': getattr(user, 'question_score', 0),
                    'answer_score': 0
                }
            
            for user in self.annotate(
                answer_score=Count('answer__answer_likes', filter=Q(answer__created_at__gte=one_week_ago))
            ).order_by('-answer_score')[:10]:
                if user.id in users_dict:
                    users_dict[user.id]['total_score'] += getattr(user, 'answer_score', 0)
                    users_dict[user.id]['answer_score'] = getattr(user, 'answer_score', 0)
                else:
                    users_dict[user.id] = {
                        'user': user,
                        'total_score': getattr(user, 'answer_score', 0),
                        'question_score': 0,
                        'answer_score': getattr(user, 'answer_score', 0)
                    }
            
            sorted_users = sorted(users_dict.values(), key=lambda x: x['total_score'], reverse=True)[:10]
            users = [item['user'] for item in sorted_users]
            
            for user in users:
                user.total_score = users_dict[user.id]['total_score']
                user.question_score = users_dict[user.id]['question_score']
                user.answer_score = users_dict[user.id]['answer_score']
            
            cache.set(cache_key, users, 60)
        return users

    def get_by_natural_key(self, username):
        return self.get(username=username)

class UserManager(BaseUserManager.from_queryset(UserQuerySet)):
    pass

# Добавляем менеджер к модели
User.add_to_class('objects', UserManager())