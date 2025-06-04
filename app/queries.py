import os
import random

import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'proj.settings')
django.setup()

from djmoney.money import Money
from django.utils import timezone
from datetime import timedelta
from django.db.models import QuerySet

from apps.ads_feedback.models import Feedback
from apps.bookings.models import Booking
from apps.ads.models import RealEstateType, Advertisement, Location
from apps.user.models.user import User


def create_users(n: int, is_landlord: bool = False):
    for i in range(1, n + 1):
        username = f"landlord{i}" if is_landlord else f"rentee{i}"
        email = f"{username}@example.com"
        password = "defaultpassword123"

        if not User.objects.filter(username=username).exists():
            User.objects.create_user(
                username=username,
                email=email,
                password=password,
                is_landlord=is_landlord,
            )


def create_realestatetypes():
    re_type = ['room', 'apartment', 'house', 'tent']
    re_objects = [RealEstateType(type=t) for t in re_type]
    RealEstateType.objects.bulk_create(re_objects)


def create_advertisements(n: int):
    landlords: QuerySet = User.objects.filter(is_landlord=True)
    advertisements = []
    for i in range(1, n + 1):
        country = "Hungary"
        city = "Budapest"
        address = f"Bartok Bela ut 3{i}"
        index = str(i) * 4
        location = (Location(country=country, city=city, address=address, index=index))
        location.save()

        real_estate_type = RealEstateType.objects.get(type="room")
        title = f"title{i}"
        description = f"description{i}"
        price = Money(str(i * 100), "HUF")
        rooms_count = i
        beds_count = i
        is_active = True
        owner = landlords[i % landlords.count()]

        advertisements.append(Advertisement(
            title=title,
            description=description,
            price=price,
            real_estate_type=real_estate_type,
            rooms_count=rooms_count,
            beds_count=beds_count,
            is_active=is_active,
            location=location,
            owner=owner,
        ))
    Advertisement.objects.bulk_create(advertisements)


def create_bookings(n: int, minus_days: int = 0):
    rentees: QuerySet = User.objects.filter(is_landlord=False)
    ads = Advertisement.objects.all()
    print('=+= ' * 90)
    # [print(a.id) for a in ads]
    print(ads.count())
    print()
    print('=+= ' * 30)
    bookings = []
    for booking_i in range(1, n + 1):
        adv_i = booking_i % Advertisement.objects.count()
        booking_date = (timezone.now().date() + timedelta(days=booking_i))
        booking_date = booking_date - timedelta(days=minus_days) if minus_days else booking_date
        bookings.append(Booking(
            start=booking_date,
            end=booking_date + timedelta(days=booking_i + 2),
            cancel_until=booking_date - timedelta(days=2),
            advertisement=ads[adv_i % ads.count()],
            rentee=rentees[booking_i % rentees.count()],
            canceled=(booking_i % 7 == 0),
            approved=(booking_i % 3 == 0),
        ))
    Booking.objects.bulk_create(bookings)

def delete_all_entities(model):
    [entity.delete() for entity in model.objects.all()]


def clear():
    delete_all_entities(Feedback)
    delete_all_entities(Booking)
    delete_all_entities(Advertisement)
    delete_all_entities(User)


def create_feedback():
    # ads = Advertisement.objects.all()
    # for ad in ads:
    rentee_ads = Booking.objects.filter(end__lte='2025-01-01').values('rentee', 'advertisement').distinct()
    feedbacks = []
    for rentee_ad in rentee_ads:
        feedbacks.append(Feedback(
            rentee=User.objects.get(pk=rentee_ad['rentee']),
            advertisement=Advertisement.objects.get(pk=rentee_ad['advertisement']),
            review_message='booking.advertisement.description',
            rating_value=random.randint(1, 10)
        ))
    Feedback.objects.bulk_create(feedbacks)


if __name__ == "__main__":
    create_users(4)
    create_users(4, True)
    create_realestatetypes()
    create_advertisements(40)
    create_bookings(100)
    create_bookings(700, 5400)
    create_feedback()
    # clear()
