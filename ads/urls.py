from django.urls import path, include
from .views import *


urlpatterns = [

    # Панель пользователя и менеджера
    path('manager/add', add_manager_view, name='add_manager'),
    path('manager/send_news', send_news_view, name='send_news'),
    path("subscription", subcribe_form_view, name="subcribe_form"),

    # Раьота с объявлениями
    path("", AdListView.as_view(), name="ad_list"),
    path("ad/create", AdCreateView.as_view(), name="ad_create"),
    path("<int:pk>", AdDetailView.as_view()),
    path("<int:pk>/edit", AdUpdateView.as_view()),

    # URLs для работы с откликами
    path("<int:ad_id>/response", ResponseCreateView.as_view(), name="response_create"),
    path("responses", ResponseListView.as_view(), name="responses"),
    path("response/<int:pk>/accept", ResponseUpdateView.as_view(), name="response_accept"),
    path("response/<int:pk>/delete", ResponseDeleteView.as_view(), name="response_delete"),

    # URL для тестирования
    path("test/", test_view, name='test'),
]