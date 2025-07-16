from django.urls import path, include
from .views import ads_view, AdListView, ResponseListView


urlpatterns = [
    path("", AdListView.as_view(), name="ad_list"),
    path("responses", AdListView.as_view(), name="responses"),
]