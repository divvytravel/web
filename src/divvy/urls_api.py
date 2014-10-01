from django.conf.urls import patterns, include, url

from rest_framework import routers

from apps.trips.api import TripViewSet, TripRequestViewSet
from apps.trips.views import triprequest_create, triprequest_cancel, triprequest_approve
from apps.users.api import UserViewSet

router = routers.DefaultRouter()
router.register(r'trips', TripViewSet)
router.register(r'triprequests', TripRequestViewSet)
router.register(r'users', UserViewSet)

urlpatterns = patterns('',
    url(r'', include(router.urls)),
    url(r'triprequest/(?P<trip_pk>\d+)/cancel/', triprequest_cancel, name='triprequest_cancel'),
    url(r'triprequest/(?P<triprequest_pk>\d+)/approve/', triprequest_approve, name='triprequest_approve'),
    url(r'triprequest/(?P<trip_pk>\d+)/', triprequest_create, name='triprequest_create'),
)
