''' Функционал по регистрации нового пользователя реализован в следующем порядке:
  1. Загрузка формы для заполнения данных пользователя
  2. Перенаправление на страницу с вводом кода
  3. Окончательная верификация почты и перенаправление на главную страницу '''


from django.urls import path
from django.contrib.auth.views import LogoutView

from allauth.account.views import (PasswordResetView, PasswordResetDoneView,
                                   PasswordResetFromKeyView, PasswordResetFromKeyDoneView)

from .views import UserRegisterView, CustomLoginView, confirm_email_view


urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(template_name='sign/logout.html'),name='logout'),

    # URLs регистрации нового пользователя
    path("signup/", UserRegisterView.as_view(), name="signup"),
    path('signup/confirm_email/<str:email>', confirm_email_view, name="confirm_email"),

    # Сброс и изменение пароля
    path('account/password/reset/',
         PasswordResetView.as_view(), name='account_reset_password'),
    path('account/password/reset/done/', PasswordResetDoneView.as_view(), name='account_reset_password_done'),
    path('account/password/reset/key/<uidb36>/<key>/', PasswordResetFromKeyView.as_view(),
         name='account_reset_password_from_key'),
    path('account/password/reset/key/done/', PasswordResetFromKeyDoneView.as_view(),
         name='account_reset_password_from_key_done'),
]