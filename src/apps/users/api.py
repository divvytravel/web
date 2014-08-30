# -*- coding:utf-8 -*-

from rest_framework import serializers, viewsets

from .models import DivvyUser

class UserSerialiser(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = DivvyUser


class UserViewSet(viewsets.ModelViewSet):
    queryset = DivvyUser.objects.all()
    serializer_class = UserSerialiser
