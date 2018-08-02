from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index, name="index"),
    path('home', views.index, name="home"),
    path('register', views.UserFormView.as_view(), name="register"),
    path('login/', auth_views.login, {'template_name':'orders/login.html'}, name="login"),
    path('logout/', auth_views.logout,  {'next_page': '/'}, name="logout"),
    path("menu", views.menu, name="menu"),
    path('food/<int:item_id>/', views.BasicFoodFormView.as_view()),
    path('checkout', views.CheckOutFormView.as_view()),
    path('carts/<int:cart_id>', views.OrderedCartView.as_view(), name="carts"),
    path('carts', views.carts, name="carts"),
]