from rest_framework import serializers
from django.utils import timezone

from .models import Booking
from ..user.models.user import User


class BookingSerializer(serializers.ModelSerializer):
    rentee = serializers.SlugRelatedField(
        slug_field='email',
        queryset=User.objects.all(),
        required=False,
    )
    landlord = serializers.CharField(
        source='advertisement.owner.email',
        read_only=True,
    )

    class Meta:
        model = Booking
        fields = "__all__"
        read_only = ['rentee', 'approved']

    def validate(self, attrs):
        cancel_until = attrs.get('cancel_until')
        start = attrs.get('start')
        end = attrs.get('end')

        if start <= cancel_until:
            raise serializers.ValidationError({"detail":"cancel_until date must be after start date."})

        if start < timezone.now().date():
            raise serializers.ValidationError({"detail":"start date must be today or in the future."})

        if end <= start:
            raise serializers.ValidationError({"detail":"end date must be after start date."})

        # Check for overlapping ranges
        overlapping = Booking.objects.filter(
            start__lt=end,
            end__gt=start,
            canceled=False,
            approved=True,
        ).values('pk')

        if overlapping.exists():
            raise serializers.ValidationError({
                    "detail":"overlapping",
                    "bookings": list(overlapping.values_list('pk', flat=True))
                })
        return attrs

