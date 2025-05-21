from typing import Any
from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(max_length=40, required=True)
    password = forms.CharField(widget=forms.PasswordInput, min_length=5, required=True)

    def clean(self) -> dict[str, Any]:
        return super().clean()


class RegisterForm(forms.Form):
    username = forms.CharField(max_length=40, required=True)
    email = forms.EmailField(required=True)
    nickname = forms.CharField(max_length=40, required=True)
    password = forms.CharField(widget=forms.PasswordInput, min_length=5, required=True)
    repeat_password = forms.CharField(widget=forms.PasswordInput, min_length=5, required=True)
    upload_avatar = forms.ImageField(required=False)