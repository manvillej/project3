from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('register', views.UserFormView.as_view(), name="register"),
    path("menu", views.menu, name="menu"),
]