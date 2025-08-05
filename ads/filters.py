from django_filters.filterset import FilterSet, CharFilter, ChoiceFilter, forms
from django_filters import filterset
from .models import Response, CATEGORIES


class ResponseFilter(FilterSet):
    ad__title = CharFilter(field_name='ad__title',
                           lookup_expr='iregex',
                           label='Заголовок объявления')
    ad__category = ChoiceFilter(
        choices=CATEGORIES,
        field_name='ad__category',
        label='Категория объявления',
        widget=forms.Select,
        )

    class Meta:
        model = Response
        fields = ['ad__title', 'ad__category']
