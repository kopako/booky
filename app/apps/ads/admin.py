from django.contrib import admin
from django.db.models import QuerySet

from . import models


@admin.register(models.Advertisement)
class AdvertisementAdmin(admin.ModelAdmin):
    list_display = ('title', 'location', 'is_active')
    search_fields = ('location__address',)
    list_filter = ('title', 'description', 'is_active',)

    actions = ['activate', 'deactivate']

    def activate(self, request, objects: QuerySet) -> None:
        for obj in objects:
            obj.is_active = True
            obj.save()

    activate.short_description = "Activate selected advertisement"

    def deactivate(self, request, objects: QuerySet) -> None:
        for obj in objects:
            obj.is_active = False
            obj.save()

    deactivate.short_description = "Deactivate selected advertisement"
