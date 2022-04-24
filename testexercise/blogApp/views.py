from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseNotFound
from django.contrib import messages
from django.contrib.auth.hashers import make_password

from blogApp.forms import *
from blogApp.models import *
from blogApp.exceptions import *


# Index page
def index(request):
    return render(request, 'blogApp/index.html')


# Страница авторизации
def login(request):
    return render(request, 'blogApp/login.html')


# Страница 404
def page_404(request, exception):
    return HttpResponseNotFound("<h2>Page not found</h2>")


# Регистрация
def register(request):
    if request.method == 'POST':
        context = {
            'registration_form': RegisterForm(request.POST),
            'email': request.POST['email'],
            'password': request.POST['password'],
            'fio': request.POST['fio']
        }
        if ValidationError.validate(ValidationError.pattern, context['password']):
            messages.success(request, """Пароль должен содержать хотя бы одну цифру, одну букву верхнего и
                                         одну букву нижнего регистра.""")
            return redirect('register')
        else:
            User.objects.create(email_of_user=context['email'],
                                password_of_user=make_password(context['password']),
                                fio_of_user=context['fio'],
                                id_of_role=RoleOfUser.objects.get(id_of_role=2))

    else:
        statuses = Status.objects.all()
    context = {
        'registration_form': RegisterForm()
    }
    return render(request, 'blogApp/register.html', context)
