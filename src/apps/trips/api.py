# -*- coding:utf-8 -*-

import django_filters
from rest_framework import filters, serializers, viewsets

from .models import Trip, TripRequest


class TripSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Trip
        fields = ('title', 'start_date', 'end_date', 'people_min_count', )


class TripFilter(django_filters.FilterSet):
    min_people = django_filters.NumberFilter(name="people_min_count", lookup_type='gte')
    max_people = django_filters.NumberFilter(name="people_min_count", lookup_type='lte')
    class Meta:
        model = Trip
        fields = ['min_people', 'max_people']


class TripViewSet(viewsets.ModelViewSet):
    queryset = Trip.objects.all()
    serializer_class = TripSerializer
    filter_class = TripFilter


class TripRequestSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = TripRequest
        fields = ('state', 'trip', 'user', 'allow_post_fb',)


class TripRequestViewSet(viewsets.ModelViewSet):
    queryset = TripRequest.objects.all()
    serializer_class = TripRequestSerializer