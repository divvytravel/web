# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext as _


class Trip(models.Model):
    title = models.CharField(verbose_name=_(u'Title'), max_length=150)

    start_date = models.DateField(verbose_name=_(u'Start date'))
    end_date = models.DateField(verbose_name=_(u'End date'))

    people_min_count = models.PositiveIntegerField(verbose_name=_(u'Min people count'))
    people_max_count = models.PositiveIntegerField(verbose_name=_(u'Max people count'))

    class Meta:
        ordering = ('start_date',)
        verbose_name = _(u'Trip')
        verbose_name_plural = _(u'Trips')
