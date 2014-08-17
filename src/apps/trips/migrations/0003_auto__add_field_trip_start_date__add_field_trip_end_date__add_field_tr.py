# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Trip.start_date'
        db.add_column(u'trips_trip', 'start_date',
                      self.gf('django.db.models.fields.DateField')(default=datetime.date.today()),
                      keep_default=False)

        # Adding field 'Trip.end_date'
        db.add_column(u'trips_trip', 'end_date',
                      self.gf('django.db.models.fields.DateField')(default=datetime.date.today()),
                      keep_default=False)

        # Adding field 'Trip.people_min_count'
        db.add_column(u'trips_trip', 'people_min_count',
                      self.gf('django.db.models.fields.PositiveIntegerField')(default=0),
                      keep_default=False)

        # Adding field 'Trip.people_max_count'
        db.add_column(u'trips_trip', 'people_max_count',
                      self.gf('django.db.models.fields.PositiveIntegerField')(default=0),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Trip.start_date'
        db.delete_column(u'trips_trip', 'start_date')

        # Deleting field 'Trip.end_date'
        db.delete_column(u'trips_trip', 'end_date')

        # Deleting field 'Trip.people_min_count'
        db.delete_column(u'trips_trip', 'people_min_count')

        # Deleting field 'Trip.people_max_count'
        db.delete_column(u'trips_trip', 'people_max_count')


    models = {
        u'trips.trip': {
            'Meta': {'ordering': "('start_date',)", 'object_name': 'Trip'},
            'end_date': ('django.db.models.fields.DateField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'people_max_count': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'people_min_count': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'start_date': ('django.db.models.fields.DateField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '150'})
        }
    }

    complete_apps = ['trips']