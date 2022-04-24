from django import forms
from blogApp.models import *


# Форма регистрации
class RegisterForm(forms.Form):
    email = forms.EmailField(label="Электронная почта", required=True)
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput(), min_length=8, required=True)
    fio = forms.CharField(label="ФИО")


# Форма авторизации
class LoginForm(forms.Form):
    email = forms.EmailField(label="Электронная почта", required=True)
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput(), required=True)
