from django.db.models.query import QuerySet
from rest_framework import permissions
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q
from django.utils import timezone

from .models import Booking
from .permissions import IsLandlordOrAdmin
from .serializers import BookingSerializer


class BookingViewSet(viewsets.ModelViewSet):
    serializer_class = BookingSerializer

    def get_queryset(self):
        queryset: QuerySet = Booking.objects.select_related('advertisement', 'rentee')
        if self.request.user.is_staff:
            return queryset
        elif self.request.user.is_landlord:
            queryset = queryset.filter(Q(advertisement__owner=self.request.user) | Q(rentee=self.request.user))
        else:
            queryset = queryset.filter(rentee=self.request.user)
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
            return Response({
                'detail': 'Booking is already approved',
                'booking': BookingSerializer(booking).data
            }, status=status.HTTP_400_BAD_REQUEST)
        booking.approved = True
        return_booking = booking.save()
        return Response({
            'detail': 'Booking approved',
            'booking': BookingSerializer(return_booking).data
        })

    @action(detail=True, methods=['post'], url_path='cancel')
    def cancel(self, request, pk=None):
        booking = self.get_object()
        if booking.canceled:
            return Response({'detail': 'Booking is already canceled'}, status=status.HTTP_400_BAD_REQUEST)
        if self.request.user != booking.rentee:
            return Response({'detail': 'It is not your booking'}, status=status.HTTP_400_BAD_REQUEST)
        if timezone.now().date() > booking.cancel_until:
            return Response(
                {'detail': f'Cancelation deadline is {booking.cancel_until}'},
                status=status.HTTP_400_BAD_REQUEST
            )
        booking.canceled = True
        booking.save()
        return Response({'detail': 'Booking canceled'})
