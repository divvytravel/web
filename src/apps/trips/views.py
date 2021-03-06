# -*- coding: utf-8 -*-

from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string

from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.users.models import DivvyUser
from .api import UserSerialiser, TripFilter, TripSerializer, TagsSerialiser
from .models import Trip, TripRequest


def trip_detail(request, pk=None):
    trip = get_object_or_404(Trip, pk=pk)

    try:
        if request.user.pk:
            triprequest = TripRequest.objects.get(trip=trip, user=request.user)
        else:
            triprequest = None
    except TripRequest.DoesNotExist:
        triprequest = None

    return render(request, 'detail.html', dict(trip=trip, triprequest=triprequest, ))


def trip_requests(request):
    if request.user.pk:
        triprequests = TripRequest.objects.filter(trip__owner=request.user)
    else:
        triprequests = None

    return render(request, 'triprequests.html', dict(triprequests=triprequests, ))


@api_view(['POST'])
@parser_classes((JSONParser,))
@permission_classes((IsAuthenticated, ))
def triprequest_create(request, trip_pk=None):
    trip = get_object_or_404(Trip, pk=trip_pk)
    allow_post_fb = request.DATA.get('allow_post_fb', False)

    try:
        triprequest = TripRequest.objects.get(trip=trip, user=request.user)

        if triprequest.state == 'cancelled':
            triprequest.state = 'pending'
            triprequest.save()
        else:
            return Response({"error": "Trip request already created", })

    except TripRequest.DoesNotExist:
        triprequest = TripRequest(trip=trip,
                                  user=request.user,
                                  state='pending',
                                  allow_post_fb=allow_post_fb)
        triprequest.save()

    if triprequest.state == 'pending':
        rendered = render_to_string("detail_includes/request_state/pending.html",
            {"triprequest": triprequest, "trip": trip, })
        return Response({"success": "OK", "html": rendered, })


@api_view(['GET'])
@parser_classes((JSONParser,))
@permission_classes((IsAuthenticated, ))
def trips_users(request):
    if 'people' in request.GET:
        user_pk = int(request.GET['people'])
        trips = [tr.trip for tr in TripRequest.objects.filter(state='approved',
                                                              user=DivvyUser.objects.get(pk=user_pk))]
    else:
        trips = TripFilter(request.GET, Trip.objects.all())

    tags = []
    for trip in trips:
        for tag in trip.tags.all():
            tags.append(tag)

    if 'tag' in request.GET and request.GET.get('tag', None):
        trips = trips.qs.filter(tags__pk=request.GET['tag'])

    ppl_sets = [trip.peoples() for trip in trips]
    users = []
    for ppls in ppl_sets:
        for ppl in ppls:
            users.append(ppl)
    users = list(set(users))

    users_api = UserSerialiser(users, many=True)
    trips_api = TripSerializer(trips, many=True, context={'request': request})
    tags_api = TagsSerialiser(tags, many=True)
    return Response({"trips": trips_api.data, "users": users_api.data, "tags": tags_api.data, })


@api_view(['POST'])
@parser_classes((JSONParser,))
@permission_classes((IsAuthenticated, ))
def triprequest_cancel(request, trip_pk=None):
    trip = get_object_or_404(Trip, pk=trip_pk)

    try:
        triprequest = TripRequest.objects.get(trip=trip, user=request.user)
        triprequest.state = 'cancelled'
        triprequest.save()
    except TripRequest.DoesNotExist:
        return Response({"error": "Trip request does not exist", })

    if triprequest.state == 'cancelled':
        rendered = render_to_string("detail_includes/request_state/new.html",
            {"triprequest": triprequest, "trip": trip, })
        return Response({"success": "OK", "html": rendered, })


@api_view(['POST'])
@parser_classes((JSONParser,))
@permission_classes((IsAuthenticated, ))
def triprequest_approve(request, triprequest_pk=None):
    try:
        triprequest = TripRequest.objects.get(pk=triprequest_pk, trip__owner=request.user)
        triprequest.approve()
    except TripRequest.DoesNotExist:
        return Response({"error": "Trip request does not exist", })

    if triprequest.state == 'approved':
        return Response({"success": "OK", })
