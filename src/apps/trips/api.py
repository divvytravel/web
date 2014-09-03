# -*- coding:utf-8 -*-

import django_filters
from rest_framework import serializers, viewsets

from .models import Trip, TripRequest


class TripSerializer(serializers.HyperlinkedModelSerializer):
    start_date = serializers.Field(source='start_date_format')
    end_date = serializers.Field(source='end_date_format')
    photos = serializers.RelatedField(many=True)
    main_photo = serializers.Field(source='get_main_photo_url')
    absolute_url = serializers.Field(source='get_absolute_url')

    class Meta:
        model = Trip
        fields = ('title', 'city', 'start_date', 'end_date',
                  'people_min_count', 'price', 'owner',
                  'main_photo', 'photos', 'absolute_url')


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