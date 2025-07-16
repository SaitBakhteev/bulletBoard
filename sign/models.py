from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth.forms import UserCreationForm
from django.forms import CharField, EmailField


# Основная форма регистрации пользователя
class UserRegisterForm(UserCreationForm):
    first_name = CharField(max_length=20, label='Имя')
    last_name = CharField(max_length=20, label='Фамилия')
    email = EmailField(max_length=50, label='Адрес электронной почты')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')