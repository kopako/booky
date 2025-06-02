from django.urls import path, include
from rest_framework import routers

from .views import BookingViewSet

app_name = "bookings"

router = routers.DefaultRouter()
router.register(r'booking', BookingViewSet, basename='booking')

urlpatterns = [
    path('', include((router.urls, app_name))),
]
