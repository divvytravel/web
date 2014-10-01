# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url
from .views import trip_detail, trip_requests

urlpatterns = patterns('',
    url(r'^(?P<pk>\d+)/$', trip_detail, name='trip_detail'),
    url(r'^requests/$', trip_requests, name='trip_requests'),
)
