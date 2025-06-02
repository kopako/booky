import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'proj.settings')
django.setup()

from djmoney.money import Money
from django.utils import timezone
from datetime import timedelta

from apps.bookings.models import Booking
from apps.ads.models import RealEstateType, Advertisement, Location
from apps.user.models.user import User


def delete_all_users():
    for u in User.objects.all():
        u.delete()


def create_users(n: int):
    for i in range(n):
        username = f"user{i}"
        email = f"user{i}@example.com"
        password = "defaultpassword123"

        if not User.objects.filter(username=username).exists():
            User.objects.create_user(
                username=username,
                email=email,
                password=password,
                is_landlord=True,
            )


def create_realestatetypes():
    re_type = ['room', 'apartment', 'house', 'tent']
    re_objects = [RealEstateType(type=t) for t in re_type]
    RealEstateType.objects.bulk_create(re_objects)


def create_advertisements(n: int):
    for i in range(n):
        country = "Hungary"
        city = "Budapest"
        address = f"Bartok Bela ut 3{i}"
        index = str(i) * 4
        location = Location(country=country, city=city, address=address, index=index).save()

        real_estate_type = RealEstateType.objects.get(type="room")
        title = f"title{i}"
        description = f"description{i}"
        price = Money(str(i * 100), "HUF")
        rooms_count = i
        beds_count = i
        is_active = True
        owner = User.objects.get(email=f"user{i}@example.com")

        advertisement = Advertisement(
            title=title,
            description=description,
            price=price,
            real_estate_type=real_estate_type,
            rooms_count=rooms_count,
            beds_count=beds_count,
            is_active=is_active,
            location=location,
            owner=owner,
        ).save()

def create_bookings(n: int):
    for booking_i in range(n):
        adv_i = (booking_i+1) % Advertisement.objects.count()
        booking_date = timezone.now().date() + timedelta(days=25)
        Booking.objects.create(
            start=booking_date,
            end=booking_date + timedelta(days=2),
            cancel_until=booking_date - timedelta(days=2),
            advertisement=Advertisement.objects.get(title=f"title{adv_i}"), # rentee != landlord
            rentee=User.objects.get(email=f"user{booking_i}@example.com"),
        ).save()


if __name__ == "__main__":
    create_users(4)
    create_realestatetypes()
    create_advertisements(4)
    create_bookings(4)
