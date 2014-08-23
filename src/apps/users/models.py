# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext as _


class DivvyUser(AbstractUser):
    birthday = models.DateField(_(u'Birthday'), blank=True, null=True)
