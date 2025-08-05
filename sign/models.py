from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
from django.forms import Form, HiddenInput
from django.forms import CharField, EmailField, IntegerField


# Основная форма регистрации пользователя
class UserRegisterForm(UserCreationForm):
    email = EmailField(max_length=50, label='Адрес электронной почты')
    first_name = CharField(max_length=20, required=False, label="введите Ваше имя")

    class Meta:
        model = User
        fields = ('first_name', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)

        # При первой регистрации до подтверждения почты пользователь пока неактивен
        user.is_active = False
        user.username = self.cleaned_data['email']
        user.save()
        return user

    def clean_email(self):
        if User.objects.filter(email=self.cleaned_data['email']).exists():
            raise ValidationError('Пользователь с таким адресом электронной почты уже зарегистрирован в системе')
        return self.cleaned_data['email']


class UserEmailConfirmedForm(Form):
    random_code = CharField(disabled=False, max_length=6)
