from django.urls import path
from .views import login, register, login_user, logout_user

app_name = 'users'

urlpatterns = [
    path('', login, name='login'),
    path('registration/', register, name='register'),
    path('logout/', logout_user, name='logout_user'),


]
