import django_filters
from django_filters import rest_framework as filters
from .models import Advertisement
from django.contrib.auth.models import User


class AdvertisementFilter(django_filters.FilterSet):
    """Фильтры для объявлений."""
    # TODO: задайте требуемые фильтры
    date_range = django_filters.DateFromToRangeFilter(field_name='created_at')
    status = django_filters.ChoiceFilter(choices=Advertisement.STATUS_CHOICES)
    creator = django_filters.ModelChoiceFilter(queryset=User.objects.all())
    created_at_before = django_filters.DateFilter(field_name='created_at', lookup_expr='lte')

    class Meta:
        model = Advertisement
        fields = ['date_range', 'status', 'creator', 'created_at_before']





