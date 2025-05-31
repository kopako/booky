from django.db import models

from ..ads.models import Advertisement
from ..user.models.user import User


class Booking(models.Model):
    start = models.DateField()
    end = models.DateField()
    cancel_until = models.DateField()
    advertisement = models.ForeignKey(Advertisement, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    approved = models.BooleanField(default=False)
    canceled = models.BooleanField(default=False)

    rentee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='booking')

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(end__gt=models.F('start')),
                name='valid_dates'
            ),
            models.UniqueConstraint(
                fields=['advertisement', 'start', 'end'],
                name='advertisement_start_end'
            )
        ]