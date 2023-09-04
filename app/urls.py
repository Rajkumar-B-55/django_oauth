from django.urls import path
from . import views

urlpatterns = [

    path('home', views.home, name='posts'),
    path('register', views.register, name='register'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('register_template', views.register_template, name='register_template'),
    path('google_signin', views.google_signin, name='G_Login'),
    path('google_signup', views.google_signup, name='G_Signup'),
    path('google_signup_callback', views.google_callback, name='G_callback'),
    path('protected_area', views.protected_area, name='G_verify'),

    path('linkedin_signin', views.linkedin_signin, name='Lin_signin'),
    path('linkedin_login', views.linkedin_login, name='Lin_login'),
    path('linkedin_signup', views.linkedin_signup, name='Lin_signup'),
    path('linkedin_authorize', views.linkedin_authorize, name='Lin_login'),

]
