# -*- coding:utf-8 -*-

import django_filters
from rest_framework import serializers, viewsets

from apps.users.api import UserSerialiser

from .models import Trip, TripRequest, Tag


class TagsSerialiser(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name', 'slug')


class TripSerializer(serializers.HyperlinkedModelSerializer):
    start_date = serializers.Field(source='start_date_format')
    end_date = serializers.Field(source='end_date_format')
    period = serializers.Field(source='period_format')
    photos = serializers.RelatedField(many=True)
    main_photo = serializers.Field(source='get_main_photo_url')
    absolute_url = serializers.Field(source='get_absolute_url')
    peoples = UserSerialiser(source='peoples', many=True)
    tags = TagsSerialiser(many=True)

    class Meta:
        model = Trip
        fields = ('title', 'city', 'start_date', 'end_date', 'period',
                  'people_min_count', 'price', 'owner', 'peoples',
                  'main_photo', 'photos', 'absolute_url', 'tags')


class TripFilter(django_filters.FilterSet):
    city = django_filters.CharFilter(name="city", lookup_type='exact')
    min_price = django_filters.NumberFilter(name="price", lookup_type='gte')
    max_price = django_filters.NumberFilter(name="price", lookup_type='lte')
    min_people = django_filters.NumberFilter(name="people_min_count", lookup_type='gte')
    max_people = django_filters.NumberFilter(name="people_min_count", lookup_type='lte')
    # tag = django_filters.NumberFilter(name="tags", lookup_type='pk')

    class Meta:
        model = Trip
        fields = ['city', 'min_price', 'max_price', 'min_people', 'max_people',]


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