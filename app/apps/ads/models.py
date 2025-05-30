from django.db import models
from djmoney.models.fields import MoneyField

# from . import managers
# from django.utils import timezone

from ..user.models.user import User


class Location(models.Model):
    country = models.CharField(max_length=50)
    city = models.CharField(max_length=50, blank=True, null=True)
    address = models.CharField(max_length=50, blank=True, null=True)
    index = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.index} {self.country} {self.city} {self.address}"


class RealEstateType(models.Model):
    type = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.type


class Advertisement(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    # images = models.JSONField(default=list, blank=True, null=True) # TODO: Add support for media. Base64 encoded?
    is_active = models.BooleanField()
    price = MoneyField(max_digits=14, decimal_places=2, default_currency='HUF')
    rooms_count = models.PositiveIntegerField()
    beds_count = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, blank=True)
    real_estate_type = models.ForeignKey(RealEstateType, models.SET_NULL, null=True, blank=True)
    owner = models.ForeignKey(User, models.CASCADE)

    # objects = managers.ActiveManager()
    # deleted = models.BooleanField(default=False) # TODO: implement deletion of related fields
    # deleted_at = models.DateTimeField(null=True, blank=True)
    # objects = managers.SoftDeleteManager()
    # def delete(self, *args, **kwargs):
    #     self.deleted = True
    #     self.deleted_at = timezone.now()
    #
    #     self.save()

    def __str__(self):
        return self.title