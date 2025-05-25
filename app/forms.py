from typing import Any
from django import forms
from django.contrib.auth.models import User

from app.models import Answer, Avatar, Profile, Question, Tag
class LoginForm(forms.Form):
    username = forms.CharField(max_length=40, required=True)
    password = forms.CharField(widget=forms.PasswordInput, min_length=5, required=True)

    def clean(self) -> dict[str, Any]:
        return super().clean()
    

class AnswerForm(forms.ModelForm):
    content = forms.CharField(required=True, min_length=10)
    
    class Meta:
        model = Answer
        fields = ['content']
    def save(self, user, question_id, commit=True):
        answer = super().save(commit=False)
        answer.author_id = user.id  
        answer.question_id = question_id
        if commit:
            answer.save() 
        return answer

class AskForm(forms.ModelForm):
    title = forms.CharField(required=True, min_length=10)
    desc = forms.CharField(required=True, min_length=10)
    tags = forms.CharField(required=True, min_length=4)
    class Meta:
        model = Question
        fields = ['title', 'desc', 'tags']
    def save(self, user, commit=True):
        question = super().save(commit=False)
        question.author_id = user.id  
        if commit:
            question.save() 
            
            tag_titles = self.cleaned_data['tags'].split(',') 
            for title in tag_titles:
                tag, _ = Tag.objects.get_or_create(title=title.strip())
                question.tags.add(tag)
        return question
        
        
    def clean(self) -> dict[str, Any]:
        return super().clean()

class SettingsForm(forms.ModelForm):
    email = forms.EmailField(required=True)
    nickname = forms.CharField(max_length=255, required=True)
    avatar = forms.ImageField(required=False)
    
    class Meta:
        model = User
        fields = ['email'] 

    def __init__(self, *args, **kwargs):
        self.profile = kwargs.pop('profile', None)
        super().__init__(*args, **kwargs)
        
        if self.profile:
            self.fields['email'].initial = self.profile.user.email
            self.fields['nickname'].initial = self.profile.nickname

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save(update_fields=['email'])
            # Обновляем профиль
            if self.profile:
                self.profile.nickname = self.cleaned_data['nickname']
                if self.cleaned_data.get('avatar'):
                    self.profile.avatar = self.cleaned_data['avatar']
                self.profile.save()
        
        return user

class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, min_length=5, required=True)
    repeated_password = forms.CharField(widget=forms.PasswordInput, min_length=5, required=True)
    avatar = forms.ImageField(required=False)
    nickname = forms.CharField(max_length=100)
    
    class Meta:
        model = User
        fields = ['username', 'email']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        repeated_password = cleaned_data.get('repeated_password')
        
        if password and repeated_password and password != repeated_password:
            self.add_error('repeated_password', "Passwords do not match")
        
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        
        if commit:
            user.save()
            avatar = None
            if self.cleaned_data['avatar']:
                avatar = Avatar.objects.create(image=self.cleaned_data['avatar'])
            Profile.objects.create(
                user=user,
                avatar=avatar,
                nickname=self.cleaned_data['nickname'],
            )
        
        return user
        