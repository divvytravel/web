# -*- coding:utf-8 -*-

from rest_framework import serializers, viewsets

from .models import DivvyUser

class UserSerialiser(serializers.HyperlinkedModelSerializer):
    avatar_url = serializers.Field(source='get_avatar_url')

    class Meta:
        model = DivvyUser
        fields = ('username', 'avatar_url')


class UserViewSet(viewsets.ModelViewSet):
    queryset = DivvyUser.objects.all()
    serializer_class = UserSerialiser
