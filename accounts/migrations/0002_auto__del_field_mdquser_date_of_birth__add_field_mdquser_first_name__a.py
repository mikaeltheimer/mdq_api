# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'MDQUser.date_of_birth'
        db.delete_column(u'accounts_mdquser', 'date_of_birth')

        # Adding field 'MDQUser.first_name'
        db.add_column(u'accounts_mdquser', 'first_name',
                      self.gf('django.db.models.fields.CharField')(default='Test', max_length=255),
                      keep_default=False)

        # Adding field 'MDQUser.last_name'
        db.add_column(u'accounts_mdquser', 'last_name',
                      self.gf('django.db.models.fields.CharField')(default='Test', max_length=255),
                      keep_default=False)


    def backwards(self, orm):

        # User chose to not deal with backwards NULL issues for 'MDQUser.date_of_birth'
        raise RuntimeError("Cannot reverse this migration. 'MDQUser.date_of_birth' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'MDQUser.date_of_birth'
        db.add_column(u'accounts_mdquser', 'date_of_birth',
                      self.gf('django.db.models.fields.DateField')(),
                      keep_default=False)

        # Deleting field 'MDQUser.first_name'
        db.delete_column(u'accounts_mdquser', 'first_name')

        # Deleting field 'MDQUser.last_name'
        db.delete_column(u'accounts_mdquser', 'last_name')


    models = {
        u'accounts.mdquser': {
            'Meta': {'object_name': 'MDQUser'},
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '255'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_admin': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        }
    }

    complete_apps = ['accounts']