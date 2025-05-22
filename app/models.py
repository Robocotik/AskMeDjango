from django.db import models
from django.contrib.auth.models import User
from django.db.models import Manager
from django.db.models import Count
from django.db.models import Prefetch
from django.core.exceptions import ObjectDoesNotExist

class Profile(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    nickname = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self) -> str:
        return self.user.username
    
class QuestionManager(Manager):
    def all_questions(self):
        return self.annotate(answer_count=Count('answers'), likes_count=Count('likes'))
    def new_questions(self):
        return self.annotate(answer_count=Count('answers'), likes_count=Count('likes')).order_by('-created_at')
    def best_questions(self):
        return self.annotate(answer_count=Count('answers'), likes_count=Count('likes')).order_by('-likes_count')
    
    def question_with_id(self, id):
        try:
            answers_with_likes = Answer.objects.annotate(likes_count=Count('answer_likes'))
            return self.prefetch_related(
            Prefetch('answers', queryset=answers_with_likes),'tags').annotate(answer_count=Count('answers'), likes_count=Count('likes')).get(id=int(id))
        except ObjectDoesNotExist:
            return None
        
    def questions_with_tag(self, tag_title):
        self = self.annotate(answer_count=Count('answers'), likes_count=Count('likes'))
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
    
class Answer(models.Model):
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
