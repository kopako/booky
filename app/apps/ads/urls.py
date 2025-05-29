from django.urls import path, include
from rest_framework import routers

from .views import LocationView, RealEstateTypeView, AdvertisementView

app_name = "ads"

router = routers.DefaultRouter()
router.register(r'location', LocationView)
router.register(r'realestate', RealEstateTypeView)
router.register(r'ads', AdvertisementView, basename='ads')

urlpatterns = [
    path('', include((router.urls, app_name))),
]
