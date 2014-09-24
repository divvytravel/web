# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext as _


class DivvyUser(AbstractUser):
    birthday = models.DateField(_(u'Birthday'), blank=True, null=True)

    def get_avatar_url(self):
        return u'http://graph.facebook.com/%s/picture?type=large&width=90&height=90' % \
               self.social_auth.get().uid
