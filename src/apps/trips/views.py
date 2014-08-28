# -*- coding: utf-8 -*-

from django.shortcuts import render, get_object_or_404

from .models import Trip

def trip_detail(request, pk=None):
    trip = get_object_or_404(Trip, pk=pk)
    return render(request, 'detail.html', dict(trip=trip,))