from django_filters import rest_framework as filters

from .models import Booking


class BookingFilter(filters.FilterSet):
    rentee = filters.CharFilter(field_name='rentee__email', lookup_expr='icontains')

    class Meta:
        model = Booking
        fields = {
            'start': ['lte', 'gte'],
            'end': ['lte', 'gte'],
            'advertisement': ['exact'],
        }
