from django.urls import path

from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('login/', login, name='login'),
    path('register/', register, name='register'),
    path('logout/', logout, name='logout'),
    path('write_post/', write_post, name='write_post'),
    path('read_posts/<int:status>', read_posts, name='read_posts')
]
