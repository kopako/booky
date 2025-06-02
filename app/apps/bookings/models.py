from django.db import models
from rest_framework import serializers

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

    def clean(self):
        super().clean()
        if self.advertisement and self.rentee and self.rentee == self.advertisement.owner:
            raise serializers.ValidationError({"model_detail": "Owner cannot book their own appartment."})

    def save(self, **kwargs):
        self.full_clean()
        super().save(**kwargs)
