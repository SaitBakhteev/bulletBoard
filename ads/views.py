from django.conf import settings

from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User, Group

from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect
from django.views.generic import DetailView, DeleteView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse

from .models import Ad, Response, Subscriber
from .forms import AdForm, ResponseForm, SubcriberForm, ConfirmManagerForm, MassSendingForm
from .tasks import weekly_mailing
from .filters import ResponseFilter

from django.core.mail import EmailMessage


# Оформление подписки на новостные рассылки по категориям
@login_required
def subcribe_form_view(request):
    subscriber = None  # сначала задаем, что пользователя нет

    if Subscriber.objects.filter(user=request.user).exists():
        subscriber = Subscriber.objects.get(user=request.user)
        form = SubcriberForm(initial={'category': subscriber.categories})
    else:
        form = SubcriberForm()

    if request.method == 'POST':
        form = SubcriberForm(request.POST)
        if form.is_valid():
            if subscriber:  # если в БД уже есть подписчик, то обновляем его категории
                subscriber.categories = form.cleaned_data['category']
                subscriber.save()
            else:  # или создаем нового подписчика
                Subscriber.objects.create(user=request.user, categories=form.cleaned_data['category'])
    return render(request, 'ads/subsribe_form.html', {'form': form})


# Заявка стать менеджером
@login_required
def add_manager_view(request):

    # Eсли пользователь уже находится в группе менеджеров
    if request.user.groups.filter(name='managers').exists():
        context = {'form': None}

    # Если пользователь не менеджер
    else:
        form = ConfirmManagerForm()
        if request.method == 'POST':
            form = ConfirmManagerForm(request.POST)
            if form.is_valid():
                group = Group.objects.get(name='managers')
                group.user_set.add(request.user)
                context = {'manager_is_added': True}
                return render(request, 'ads/modal and any forms/manager.html', context)
        context = {'form': form}
    return render(request, 'ads/modal and any forms/manager.html', context)


# Массовая рассылка новостей всем пользователям
@login_required
@permission_required('ads.can_send_mass_email', raise_exception=True)
def send_news_view(request):
    form = MassSendingForm()
    if request.method == 'POST':
        form = MassSendingForm(request.POST)
        if form.is_valid():
            subject, text = form.cleaned_data['subject'], form.cleaned_data['text']
            recepients = (User.objects.values_list('email', flat=True).filter(is_active=True))
            message = EmailMessage(subject=subject,
                            body=text,
                            from_email=settings.DEFAULT_FROM_EMAIL,
                            to=[settings.DEFAULT_FROM_EMAIL],
                            bcc=list(recepients),)
            message.send()
            return render(request, 'ads/modal and any forms/mass_send.html')
    return render(request, 'ads/modal and any forms/mass_send.html', {'form': form})


# Список объявлений (лендинг)
class AdListView(ListView):
    model = Ad
    template_name = 'ads/ads.html'
    context_object_name = 'ad'
    ordering = ['-created_at']
    paginate_by = 5


class AdDetailView(DetailView):
    model = Ad
    success_url = reverse_lazy('ad_list')
    form_class = AdForm
    context_object_name = 'ad'
    template_name = 'ads/ad_card.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.user.is_authenticated:
            ad = self.get_object()

            # Если есть отклик от данного пользователя на данное объявление
            if Response.objects.filter(ad=ad, author=self.request.user).exists():
                response = Response.objects.get(ad=ad, author=self.request.user)
                context['response'] = response
        return context


''' Вьюхи только для авторизованных пользователей '''

# Создание объявления
class AdCreateView(LoginRequiredMixin, CreateView):
    model = Ad
    success_url = reverse_lazy('ad_list')
    form_class = AdForm
    template_name = 'ads/ad_create_update.html'

    def form_valid(self, form):
        form.instance.author = self.request.user  # Привязываем текущего пользователя
        return super().form_valid(form)


# Редактирование объявления
class AdUpdateView(LoginRequiredMixin, UpdateView):
    model = Ad
    success_url = reverse_lazy('ad_list')
    form_class = AdForm
    template_name = 'ads/ad_create_update.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_update'] = True
        return context


# Список откликов
class ResponseListView(LoginRequiredMixin, ListView):
    model = Response
    template_name = 'ads/responses.html'
    context_object_name = 'responses'
    filter_class = ResponseFilter
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset().filter(ad__author=self.request.user)
        self.filter = self.filter_class(self.request.GET, queryset=queryset)

        return self.filter.qs.order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = self.filter.form
        return context


class ResponseCreateView(LoginRequiredMixin, CreateView):
    model = Response
    form_class = ResponseForm
    template_name = 'ads/ad_card.html'
    success_url = reverse_lazy('ad_list')
    context_object_name = 'response_form'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Мы присваиваем представление от карточки объявления
        ad_view = AdDetailView()
        ad_view.request, ad_view.kwargs = self.request, {'pk': self.kwargs['ad_id']}
        ad_view.object = ad_view.get_object()  # не совсем понимаю почему, но эта строка нужна
        context.update(ad_view.get_context_data())

        context['response_create'] = True  # флаг, открывающий форму отправки отклика
        return context

    def form_valid(self, form):
        form.instance.author = self.request.user
        ad_id = self.kwargs['ad_id']  # это id объявления, извлекаемый из URL
        form.instance.ad = Ad.objects.get(id=ad_id)
        form.save()
        return super().form_valid(form)


# Принять отклик

class ResponseUpdateView(LoginRequiredMixin, UpdateView):
    model = Response
    success_url = reverse_lazy('responses')
    template_name = 'ads/modal and any forms/confirm_response_accept.html'
    fields = []

    def dispatch(self, request, *args, **kwargs):
        try:

            ''' Дополнительная проверка, чтобы пользователь не мог производить
            манипуляции с откликом на чужое объявление '''

            if self.request.user == self.get_object().ad.author:
                return super().dispatch(request, *args, **kwargs)
            else:
                raise PermissionDenied('Запрещено работать с откликами на чужие объявления')
        except PermissionDenied:
            return redirect('responses')

    def form_valid(self, form):
        form.instance.is_accepted = True
        return super().form_valid(form)

    # def get(self, request, *args, **kwargs):
    #     return HttpResponseNotAllowed(['POST'])  # Блокируем GET-запросы

# Принять отклик
def accept_response_view(request, pk):
    response = Response.objects.get(pk=pk)
    response.is_accepted = True
    response.save()
    return redirect('responses')


# Удаление отклика
class ResponseDeleteView(LoginRequiredMixin, DeleteView):
    model = Response
    success_url = reverse_lazy('responses')

    def dispatch(self, request, *args, **kwargs):
        try:
            if self.request.user == self.get_object().ad.author:
                return super().dispatch(request, *args, **kwargs)
            else:
                raise PermissionDenied('Нельзя удалять отклики на чужие объявления')
        except PermissionDenied:
            return redirect('responses')


''' Для тестирования '''
@login_required
@permission_required('bulletBoard.can_send_mass_email', raise_exception=True)
def test_view(request):
    return render(request, 'test.html')


def ads_view(request):
    context = weekly_mailing()
    return render(request, 'ads/modal and any forms/msg.html', {'user': 'mhggh'})
