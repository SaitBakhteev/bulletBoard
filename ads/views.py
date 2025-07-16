from django.shortcuts import render
from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin

from ads.models import Ad, Response


def ads_view(request):
    return render(request, 'ad.html')


# Список объявлений
class AdListView(ListView):
    model = Ad
    template_name = 'ads/ads.html'
    context_object_name = 'ads'
    queryset = Ad.objects.all()


# Список откликов
class ResponseListView(LoginRequiredMixin, ListView):
    model = Response
    template_name = 'responses/response.html'
    context_object_name = 'responses'

    def get_queryset(self):
        # Фильтрация по объявлениям текущего пользователя
        return Response.objects.filter(ad__author=self.request.user)