from django.contrib import admin
from django.contrib.contenttypes import generic

from apps.trips.models import Trip, Photo, Tag, TripRequest


class PhotoInline(generic.GenericStackedInline):
    model = Photo
    extra = 1


class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', )


class TripAdmin(admin.ModelAdmin):
    list_display = ('title', 'start_date', 'end_date', 'owner', 'created_by', )
    inlines = [PhotoInline, ]

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        obj.save()


class TripRequestAdmin(admin.ModelAdmin):
    list_display = ('state', 'trip', 'user', 'allow_post_fb', )

admin.site.register(Tag, TagAdmin)
admin.site.register(Trip, TripAdmin)
admin.site.register(TripRequest, TripRequestAdmin)
