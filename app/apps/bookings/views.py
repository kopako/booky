from django.db.models.query import QuerySet
from rest_framework import permissions
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Booking
from .permissions import IsLandlordOrAdmin
from .serializers import BookingSerializer


class BookingViewSet(viewsets.ModelViewSet):
    serializer_class = BookingSerializer
    # permission_classes = [permissions.IsAuthenticated, IsLandlordOrAdmin]

    def get_queryset(self):
        queryset: QuerySet = Booking.objects.select_related('advertisement', 'rentee')
        # queryset = queryset.filter(rentee=self.request.user)
        # if not self.request.user.is_staff:
        #     queryset = queryset.filter(is_active=True)
        return queryset

    def get_permissions(self):
        if self.action == 'approve':
            return [IsLandlordOrAdmin()]
        return [permissions.IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save(rentee=self.request.user)

    @action(detail=True, methods=['post'], url_path='approve')
    def approve(self, request, pk=None):
        booking = self.get_object()
        if booking.approved:
            return Response({'detail': 'Booking is already approved'}, status=status.HTTP_400_BAD_REQUEST)
        booking.approved = True
        booking.save()
        return Response({'detail': 'Booking approved'})

    @action(detail=True, methods=['post'], url_path='cancel')
    def cancel(self):
        booking = self.get_object()
        if booking.canceled:
            return Response({'detail': 'Booking is already canceled'}, status=status.HTTP_400_BAD_REQUEST)
        if self.request.user != booking.rentee:
            return Response({'detail': 'It is not your booking'},status=status.HTTP_400_BAD_REQUEST)
        booking.canceled = True
        booking.save()
        return Response({'detail': 'Booking approved'})
