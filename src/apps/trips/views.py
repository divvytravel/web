# -*- coding: utf-8 -*-

from django.shortcuts import render, get_object_or_404

from .models import Trip, TripRequest

def trip_detail(request, pk=None):
    trip = get_object_or_404(Trip, pk=pk)

    try:
        if request.user:
            triprequest = TripRequest.objects.get(trip=trip, user=request.user)
        else:
            triprequest = None
    except TripRequest.DoesNotExist:
        triprequest = None

    return render(request, 'detail.html', dict(trip=trip, triprequest=triprequest, ))