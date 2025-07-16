from django.shortcuts import render
from django.views.generic import CreateView
from django.contrib.auth.models import User
from .models import UserRegisterForm

# Представление для регистрации пользователя
class UserRegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'sign/signup.html'
    success_url = '/'
