# -*- coding: utf-8 -*-

import uuid

from django.conf import settings
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import ugettext as _


def get_file_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = "photos/%s.%s" % (uuid.uuid4(), ext)
    return filename


class Photo(models.Model):
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')
    image = models.ImageField(upload_to=get_file_path, max_length=255)


class Tag(models.Model):
    name = models.CharField(_(u'Tag name'), max_length=20)
    slug = models.SlugField(_(u'Slug'), unique=True)

    def __unicode__(self):
        return u'%s' % self.name


class Trip(models.Model):
    title = models.CharField(verbose_name=_(u'Title'), max_length=150)

    city = models.CharField(verbose_name=_(u'City'), max_length=150)

    start_date = models.DateField(verbose_name=_(u'Start date'))
    end_date = models.DateField(verbose_name=_(u'End date'))
    end_group_date = models.DateField(verbose_name=_(u'End group date'))

    price = models.PositiveIntegerField(_(u'Budget'), blank=True, null=True)

    people_min_count = models.PositiveIntegerField(verbose_name=_(u'Min people count'))
    people_max_count = models.PositiveIntegerField(verbose_name=_(u'Max people count'))

    description_main = models.TextField(_(u'Trip description'))

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_(u'Owner'), related_name='ownerd_trips',
                              blank=True, null=True)

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_(u'Created by user'), editable=False,
                                   related_name='created_trips')
    created_at = models.DateTimeField(auto_now_add=True)

    photos = generic.GenericRelation(Photo)
    tags = models.ManyToManyField(Tag, related_name='tag_trips', blank=True, verbose_name=_(u'Tags'))

    class Meta:
        ordering = ('start_date',)
        verbose_name = _(u'Trip')
        verbose_name_plural = _(u'Trips')
