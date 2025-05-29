from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.db.models.query import QuerySet

from .serializers import LocationSerializer, RealEstateTypeSerializer, AdvertisementSerializer
from .models import (Location, RealEstateType, Advertisement)


class LocationView(viewsets.ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class RealEstateTypeView(viewsets.ModelViewSet):
    queryset = RealEstateType.objects.all()
    serializer_class = RealEstateTypeSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class AdvertisementView(viewsets.ModelViewSet):
    serializer_class = AdvertisementSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset: QuerySet = Advertisement.objects.select_related('location', 'real_estate_type', 'owner')
        if not self.request.user.is_staff:
            queryset = queryset.filter(is_active=True)
        return queryset

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user, is_active=True)