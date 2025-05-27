from django.db import models
from django.contrib.auth.models import User
from django.db.models import Manager
from django.db.models import Count
from django.db.models import Prefetch
from django.core.exceptions import ObjectDoesNotExist

from askme_startkin.settings import MEDIA_URL
from django.db.models import Case, When, Value, CharField, F
from django.db.models.functions import Concat


class Avatar(models.Model):
    image = models.ImageField(upload_to='uploads/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

class ProfileManager(Manager):
    def profile_with_id(self, id):
        try:
            return Profile.objects.get(id=int(id))

        except ObjectDoesNotExist:
            return None
    
    def get_avatar_url(self, user):
        try:
            profile = Profile.objects.get(user=user)
            if profile.avatar and profile.avatar.image:
                return profile.avatar.image.url
        except (AttributeError, Profile.DoesNotExist):
            pass
        return '/static/empty_avatar.jpg'
        
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
            queryset = queryset.annotate(
                isLiked=Case(
                    When(
                        likes__user=user,  # Исправлено здесь
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
        
        return queryset.prefetch_related('tags')
    
    def new_questions(self):
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
            )
        ).order_by('-created_at')
    
    def best_questions(self):
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
            )
        ).order_by('-likes_count')
    
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
        
        return self.filter(tags=tag)
    

    
class Question(models.Model):
    id = models.BigAutoField(primary_key=True, editable=False)
    objects = QuestionManager()
    title = models.CharField(max_length=1000, default='title_placeholder')
    desc  = models.CharField(max_length=20000, default='desc_placeholder')
    author = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    tags = models.ManyToManyField('Tag', related_name='questions')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self) -> str:
        return self.title

class Tag(models.Model):
    title = models.CharField(max_length=255)

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
                )
        )
    # Profile.objects.get_avatar_url(user=answers[0].author)
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
