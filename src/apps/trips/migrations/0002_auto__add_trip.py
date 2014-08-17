# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Trip'
        db.create_table(u'trips_trip', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=150)),
        ))
        db.send_create_signal(u'trips', ['Trip'])


    def backwards(self, orm):
        # Deleting model 'Trip'
        db.delete_table(u'trips_trip')


    models = {
        u'trips.trip': {
            'Meta': {'object_name': 'Trip'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '150'})
        }
    }

    complete_apps = ['trips']