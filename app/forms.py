from typing import Any
from django import forms
from django.contrib.auth.models import User

from app.models import Avatar, Profile
class LoginForm(forms.Form):
    username = forms.CharField(max_length=40, required=True)
    password = forms.CharField(widget=forms.PasswordInput, min_length=5, required=True)

    def clean(self) -> dict[str, Any]:
        return super().clean()


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
        