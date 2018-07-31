from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index, name="index"),
    path('home', views.index, name="home"),
    path('register', views.UserFormView.as_view(), name="register"),
    path('login/', auth_views.login, {'template_name':'orders/login.html'}, name="login"),
    path("menu", views.menu, name="menu"),
]