# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext as _

class Trip(models.Model):
    title = models.CharField(verbose_name=_(u'Title'), max_length=150)