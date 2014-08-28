# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url
from .views import trip_detail

urlpatterns = patterns('',
    url(r'^(?P<pk>\d+)/$', trip_detail, name='trip_detail'),
)
