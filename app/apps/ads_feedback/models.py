from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from rest_framework import serializers
from django.utils import timezone
from django.db.models import QuerySet

from ..ads.models import Advertisement
from ..bookings.models import Booking
from ..user.models.user import User


class Feedback(models.Model):
    rentee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='feedback')
    advertisement = models.ForeignKey(Advertisement, on_delete=models.CASCADE)
    rating_value = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    review_message = models.TextField(blank=True, null=True)

    def clean(self):
        super().clean()
        booking: QuerySet = Booking.objects.filter(rentee=self.rentee, advertisement=self.advertisement)
        if not booking.exists():
            raise serializers.ValidationError({
                'detail': "This user haven't rent this property."
            })

        if not booking.filter(end__lte=timezone.now().date(), canceled=False, approved=True).exists():
            raise serializers.ValidationError({
                'detail': "This user haven't finished renting this property."
            })

    def save(self, **kwargs):
        self.full_clean()
        super().save(**kwargs)


    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['rentee', 'advertisement'],
                name='unique_rentee_advertisement',
                violation_error_message="Only one feedback per property per rentee"
            )
        ]
