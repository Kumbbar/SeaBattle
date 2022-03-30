from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
# Create your views here.
from .servises.auth import login_user, register_user, logged_out
from django.contrib.auth import logout


def login(request):
    """ВХОД ПОЛЬЗОВАТЕЛЯ"""
    return login_user(request)


def register(request):
    """РЕГИСТРАЦИЯ ПОЛЬЗОВАТЕЛЯ"""
    return register_user(request)


def logout_user(request):
    logged_out(request)
    return redirect('users:login')
