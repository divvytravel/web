# -*- coding: utf-8 -*-

from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string

from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


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
            {"triprequest": triprequest})
        return Response({"success": "OK", "html": rendered, })

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
            {"triprequest": triprequest})
        return Response({"success": "OK", "html": rendered, })