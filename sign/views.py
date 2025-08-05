from django.urls import reverse
from django.views.generic.edit import CreateView

from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, render

from .forms import ConfirmEmailForm, CustomAuthenticationForm
from .models import UserRegisterForm
from .functions import send_code

# Представление для регистрации пользователя
class UserRegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'sign/signup.html'

    def form_valid(self, form):
        user = form.save(commit=True)
        send_code(user.email)
        return redirect('confirm_email', email=user.email)


# Переопределение класса авторизации пользователя
class CustomLoginView(LoginView):
    form_class = CustomAuthenticationForm
    template_name = 'sign/login.html'  # Убедитесь, что указан правильный шаблон

    def form_invalid(self, form):

        ''' почему в этой строке email=username? Здесь нет путаницы. Дело в том,
        что "из коробки" для аутентификации используется username. Поэтому я у
        себя кастомно переделал, при регистрации username автоматически
        приравнивается к email '''

        email = form.data['username']

        if User.objects.filter(username=email).exists():
            send_code(email)
            return redirect('confirm_email', email=email)
        return super().form_invalid(form)


# Отображение формы для подтверждения почты
def confirm_email_view(request, email):
    form = ConfirmEmailForm(email=email)
    if request.method == 'POST':
        form = ConfirmEmailForm(request.POST, email=email)
        if form.is_valid():
            user = User.objects.get(email=email)
            user.is_active = True
            user.save()
            return redirect('login')
    return render(request, 'sign/confirm_email.html', {'form': form})
