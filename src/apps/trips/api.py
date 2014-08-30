# -*- coding:utf-8 -*-

from rest_framework import routers, serializers, viewsets

from .models import Trip

class TripSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Trip
        fields = (
            'title', 'start_date', 'end_date', )


class TripViewSet(viewsets.ModelViewSet):
    queryset = Trip.objects.all()
    serializer_class = TripSerializer


router = routers.DefaultRouter()
router.register(r'trips', TripViewSet)