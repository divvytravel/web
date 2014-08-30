from django.contrib import admin
from django.contrib.contenttypes import generic

from apps.trips.models import Trip, Photo


class PhotoInline(generic.GenericStackedInline):
    model = Photo
    extra = 1


class TripAdmin(admin.ModelAdmin):
    list_display = ('title', 'start_date', 'end_date', 'owner', 'created_by', )
    inlines = [PhotoInline, ]

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        obj.save()

admin.site.register(Trip, TripAdmin)
