from django.utils import timezone
from rest_framework import serializers

from .models import Booking
from ..user.models.user import User


class BookingSerializer(serializers.ModelSerializer):
    rentee = serializers.SlugRelatedField(
        slug_field='email',
        queryset=User.objects.all(),
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
        if cancel_until and start and end and not (timezone.now().date() < cancel_until < start < end):
            raise serializers.ValidationError(
                {"start and end": f"{timezone.now()} < {cancel_until} < {start} < {end}"}
            )
        return attrs

