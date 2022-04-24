from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password

from blogApp.forms import *
from blogApp.models import *
from blogApp.exceptions import *


# Index page
def index(request):
    return render(request, 'blogApp/index.html')


# Страница авторизации
def login(request):
    if request.method == 'POST':
        context = {
            'login_form': LoginForm(request.POST),
            'email': request.POST['email'],
            'password': request.POST['password']
        }
        email = context['email']
        user = User.objects.filter(email_of_user=email)
        if user:
            password = user[0].password_of_user
            if check_password(context['password'], password):
                request.session['loggedin'] = True
                request.session['id'] = user[0].id_of_user
                role_id = user[0].id_of_role
                request.session['role'] = role_id.id_of_role
                return HttpResponseRedirect('index')
            else:
                messages.success(request, "Пароль неверный")
        else:
            messages.success(request, "Пользователя с такой электронной почтой не существует")
    else:
        context = {
            'login_form': LoginForm()
        }
    return render(request, 'blogApp/login.html', context)


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
            return redirect('login')

    else:
        statuses = Status.objects.all()
    context = {
        'registration_form': RegisterForm()
    }
    return render(request, 'blogApp/register.html', context)
