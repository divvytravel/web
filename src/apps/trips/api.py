# -*- coding:utf-8 -*-

from rest_framework import routers, serializers, viewsets

from .models import Trip, TripRequest


class TripSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Trip
        fields = ('title', 'start_date', 'end_date', )


class TripViewSet(viewsets.ModelViewSet):
    queryset = Trip.objects.all()
    serializer_class = TripSerializer


class TripRequestSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = TripRequest
        fields = ('state', 'trip', 'user', 'allow_post_fb',)


class TripRequestViewSet(viewsets.ModelViewSet):
    queryset = TripRequest.objects.all()
    serializer_class = TripRequestSerializer


router = routers.DefaultRouter()
router.register(r'trips', TripViewSet)
router.register(r'triprequests', TripRequestViewSet)