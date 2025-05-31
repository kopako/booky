from rest_framework import serializers

from .models import (Advertisement, Location, RealEstateType)
from ..user.models.user import User

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = "__all__"

class RealEstateTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = RealEstateType
        fields = "__all__"

class AdvertisementSerializer(serializers.ModelSerializer):
    location = LocationSerializer()
    real_estate_type = serializers.SlugRelatedField(
        slug_field='type',
        queryset=RealEstateType.objects.all()
    )
    owner = serializers.SlugRelatedField(
        slug_field='email',
        queryset=User.objects.all(),
        required=False,
    )

    class Meta:
        model = Advertisement
        fields = "__all__"

    def create(self, validated_data):
        location_data = validated_data.pop('location')
        location, _ = Location.objects.get_or_create(**location_data)
        adv, _ = Advertisement.objects.get_or_create(location=location, **validated_data)
        return adv

    def update(self, instance, validated_data):
        location_data = validated_data.pop('location', None)
        if location_data:
            location, _ = Location.objects.get_or_create(**location_data)
            instance.location = location
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

