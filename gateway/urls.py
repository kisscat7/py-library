from django.urls import path
from . import views

urlpatterns = [
    path('register', views.Register, name="gateway_register"),
    path('login', views.Login, name="gateway_login"),
    path('exit', views.Exit, name="gateway_exit"),
]
