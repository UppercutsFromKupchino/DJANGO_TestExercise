import datetime

from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.contrib import messages
# from django.contrib.auth.hashers import make_password, check_password

from .forms import *
from .models import *
from .exceptions import *


# Index page
def index(request):
    if 'loggedin' in request.session and request.session['role'] == 1:
        context = {
            'role': request.session['role']
        }
        return render(request, 'blogApp/index.html', context)
    else:
        return render(request, 'blogApp/index.html')


# Страница авторизации
def login(request):
    if request.method == 'POST':
        # print(request.META['HTTP_AUTHORIZATION'])
        # Здесь будет Basic Auth
        context = {
            'login_form': LoginForm(request.POST),
            'email': request.POST['email'],
            'password': request.POST['password']
        }

        email = context['email']
        user = User.objects.filter(email_of_user=email)  # Получение пользователя из базы данных

        if user:  # Проверка на наличие пользователя
            password = user[0].password_of_user
            if context['password'] == password:  # Проверка на совпадение пароля
                request.session['loggedin'] = True  # 'loggedin' in request.session - авторизация пользователя
                request.session['id'] = int(user[0].id_of_user)
                role_id = user[0].id_of_role
                request.session['role'] = int(role_id.id_of_role)
                return redirect('index')
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
        if ValidationError.validate(ValidationError.pattern, context['password']):  # Проверка пароля на символы
            messages.success(request, """Пароль должен содержать хотя бы одну цифру, одну букву верхнего и
                                         одну букву нижнего регистра.""")
            return redirect('register')
        else:
            User.objects.create(email_of_user=context['email'],
                                password_of_user=context['password'],
                                fio_of_user=context['fio'],
                                id_of_role=RoleOfUser.objects.get(id_of_role=2))
            return redirect('login')

    else:
        context = {
            'registration_form': RegisterForm()
        }
        return render(request, 'blogApp/register.html', context)


# Написать статью
def write_post(request):
    if 'loggedin' in request.session and request.session['role'] == 1:
        if request.method == 'POST':
            print(request.POST['status'])
            context = {
                'write_post_form': WritePostForm(request.POST),
                'status': request.POST['status'],
                'text': request.POST['text']
            }
            # try:
            Post.objects.create(text_of_post=context['text'],
                                id_of_author=User.objects.get(id_of_user=request.session['id']),
                                datetime_of_post=datetime.datetime.now(),
                                id_of_status=Status.objects.get(id_of_status=context['status']))
            messages.success(request, "Запись добавлена успешно")
            return redirect('write_post')
            # except:
            #     messages.error(request, "Ошибка взаимодействия с базой данных")
            #     return redirect('write_post')
        else:
            context = {
                'write_post_form': WritePostForm()
            }
            return render(request, 'blogApp/write_post.html', context)
    else:
        messages.success(request, "У вас недостаточно прав, чтобы посещать данную страницу")
        return redirect('index')


# Страница со статьями для неавторизированных пользователей
def read_posts(request, status):
    if 'loggedin' not in request.session and status == 1:  # Неавторизированный юзер смотрит закрытые статьи
        messages.error(request, "У вас недостаточно прав, чтобы посещать данную страницу")
        return redirect('index')
    else:
        posts = Post.objects.raw(f"""SELECT * FROM post LEFT JOIN _user_ ON post.id_of_author=_user_.id_of_user WHERE 
                                     post.id_of_status={status}""")
        if 'loggedin' not in request.session:
            context = {
                'posts': posts
            }
        else:
            context = {
                'posts': posts,
                'role': request.session['role']  # Если пользователь - автор, роль - 1, добавляются кнопки удалить и редактировать
            }
        return render(request, 'blogApp/read_posts.html', context)


# Выход из системы
def logout(request):
    request.session.pop('id')
    request.session.pop('loggedin')
    request.session.pop('role')
    return redirect('index')
