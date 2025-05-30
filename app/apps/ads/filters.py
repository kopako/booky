from django_filters import rest_framework as filters

from .models import Advertisement


class AdvertisementFilter(filters.FilterSet):
    country = filters.CharFilter(field_name='location__country', lookup_expr='icontains')
    city = filters.CharFilter(field_name='location__city', lookup_expr='icontains')
    address = filters.CharFilter(field_name='location__address', lookup_expr='icontains')
    real_estate_type = filters.CharFilter(field_name='real_estate_type__type', lookup_expr='exact')
    owner = filters.CharFilter(field_name='owner__email', lookup_expr='icontains')

    class Meta:
        model = Advertisement
        fields = {
            'price': ['lte', 'gte'],
            'rooms_count': ['lte', 'gte'],
        }
