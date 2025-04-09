from django.db import models
from django.contrib.auth.models import User
from django.db.models import Manager
class Profile(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=True)
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)

    def __str__(self) -> str:
        return self.user
    
class QuestionManager(Manager):
    def new_questions(self):
        return self.order_by('-created_at')
    def best_questions(self):
        # Здесь можно добавить логику для определения "лучших" вопросов
        # Например, можно использовать количество лайков или комментариев
        return self.order_by('-likes_count')  # Пример, если у вас есть поле likes_count
    
class Question(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(User, on_delete=models.PROTECT, blank=True, null=True)
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
    question = models.ForeignKey('Question', on_delete=models.PROTECT, related_name='answers', blank=True, null=True)
    author = models.ForeignKey(User, on_delete=models.PROTECT, blank=True, null=True)
    content = models.CharField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.question
    
class QuestionLike(models.Model):
    question = models.ForeignKey('Question', on_delete=models.PROTECT, related_name='likes', blank=True, null=True)
    like = models.ForeignKey('Like', on_delete=models.PROTECT, blank=True, null=True)
    class Meta:
        unique_together = ('like', 'question')  # Исправлено на 'like' и 'question'
class AnswerLike(models.Model):
    answer = models.ForeignKey('Answer', on_delete=models.PROTECT, related_name='likes', blank=True, null=True)
    like = models.ForeignKey('Like', on_delete=models.PROTECT, blank=True, null=True)
    class Meta:
        unique_together = ('answer', 'like')  # Исправлено на 'answer' и 'like'


class Like(models.Model):
    count = models.BigIntegerField(default=0)