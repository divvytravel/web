from django.contrib import admin
from django.contrib.contenttypes import generic

from apps.trips.models import Trip, Photo


class PhotoInline(generic.GenericStackedInline):
    model = Photo
    extra = 1


class TripAdmin(admin.ModelAdmin):
    list_display = ('title', 'start_date', 'end_date')
    inlines = [PhotoInline, ]


admin.site.register(Trip, TripAdmin)
