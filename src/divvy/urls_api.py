from django.conf.urls import patterns, include, url

from rest_framework import routers

from apps.trips.api import TripViewSet, TripRequestViewSet
from apps.users.api import UserViewSet

router = routers.DefaultRouter()
router.register(r'trips', TripViewSet)
router.register(r'triprequests', TripRequestViewSet)
router.register(r'users', UserViewSet)

urlpatterns = patterns('',
    url(r'', include(router.urls)),
)
