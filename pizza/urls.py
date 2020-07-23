from django.urls import path

from . import views

urlpatterns = [
    path("",views.index,name="index"),
    path("login",views.login_view,name="login_view"),
    path("register",views.register,name="register"),
    path("menu",views.menu,name="menu"),
    path("orders",views.orders,name="orders"),
    path("myorders/<username>",views.myorders,name="myorders"),
    path("logout_view",views.logout_view,name="logout_view"),
    path("menu1",views.menu1,name="menu1"),
]