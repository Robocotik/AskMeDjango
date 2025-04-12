from django.db import models
from django.contrib.auth.models import User
from django.db.models import Manager
from django.db.models import Count
from django.core.exceptions import ObjectDoesNotExist

class Profile(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)

    def __str__(self) -> str:
        return self.user.username
    
class QuestionManager(Manager):
    # questions_with_answer_count = Question.objects.annotate(answer_count=Count('answers'))
    def all_questions(self):
        return self.annotate(answer_count=Count('answers'))
    def new_questions(self):
        return self.annotate(answer_count=Count('answers')).order_by('-created_at')
    def best_questions(self):
        return self.annotate(answer_count=Count('answers')).order_by('-likes_count')
    
    def question_with_id(self, id):
        try:
            return self.prefetch_related('answers', 'tags').annotate(answer_count=Count('answers')).get(id=int(id))
        except ObjectDoesNotExist:
            return None
        
    def questions_with_tag(self, tag_title):
        self = self.annotate(answer_count=Count('answers'))
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
    like_count = models.IntegerField(default=1)
    
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
    answer = models.ForeignKey('Answer',default=None, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(User, default=None, on_delete=models.CASCADE)
    class Meta:
        unique_together = ('answer', 'user')
