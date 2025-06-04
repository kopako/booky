from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import filters
from django.db.models.query import QuerySet
import django_filters

from .filters import AdvertisementFilter
from .serializers import LocationSerializer, RealEstateTypeSerializer, AdvertisementSerializer
from .models import (Location, RealEstateType, Advertisement)
from .permissions import IsOwner, IsLandlord


class LocationView(viewsets.ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class RealEstateTypeView(viewsets.ModelViewSet):
    queryset = RealEstateType.objects.all()
    serializer_class = RealEstateTypeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class AdvertisementView(viewsets.ModelViewSet):
    serializer_class = AdvertisementSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend, filters.OrderingFilter)
    filterset_class = AdvertisementFilter
    ordering = 'title'
    search_fields = ['title', 'description']
    ordering_fields = ['price', 'created_at', 'rooms_count', 'real_estate_type', 'beds_count']

    def get_queryset(self):
        queryset: QuerySet = Advertisement.objects.select_related('location', 'real_estate_type', 'owner')
        if not self.request.user.is_staff:
            queryset = queryset.filter(is_active=True)
        return queryset

    def get_permissions(self):
        if self.request.method in ('PATCH', 'PUT', 'DELETE'):
            permission_classes = [IsOwner, IsLandlord]
        elif self.request.method in ('POST',):
            permission_classes = [IsLandlord,]
        else:
            permission_classes = [permissions.IsAuthenticated,]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user, is_active=True)

    @action(detail=False, methods=['get'], url_path='my')
    def recent_users(self, request):
        objs = self.get_queryset().filter(owner=request.user)
        serializer = AdvertisementSerializer(objs, many=True)
        return Response(serializer.data)
