from django.contrib import admin

from .models import Tag, Answer, Question, AnswerLike, QuestionLike, Profile, Like, QuestionManager
admin.site.register(Tag)
admin.site.register(Answer)
admin.site.register(Question)
admin.site.register(Profile)
admin.site.register(Like)
# admin.site.register(AnswerLike)
# admin.site.register(QuestionLike)
# admin.site.register(QuestionManager)

