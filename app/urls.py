from django.urls import path
from . import views

urlpatterns = [

    path('home', views.home, name='posts'),
    path('register', views.register, name='register'),
    path('login', views.login, name='login'),
    path('register_template', views.register_template, name='register_template'),
    path('logout', views.logout, name='logout'),
]
