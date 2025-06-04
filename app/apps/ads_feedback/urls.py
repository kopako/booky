from django.urls import path, include
from rest_framework import routers

from .views import FeedbackViewSet

app_name = "bookings"

router = routers.DefaultRouter()
router.register(r'feedback', FeedbackViewSet, basename='feedback')

urlpatterns = [
    path('', include((router.urls, app_name))),
]
