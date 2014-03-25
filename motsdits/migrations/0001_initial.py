# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Action'
        db.create_table(u'motsdits_action', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('approved', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('flags', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.utcnow)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.utcnow)),
            ('created_by', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['accounts.MDQUser'])),
            ('score', self.gf('django.db.models.fields.FloatField')()),
            ('verb', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal(u'motsdits', ['Action'])

        # Adding model 'Tag'
        db.create_table(u'motsdits_tag', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('approved', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('flags', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.utcnow)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.utcnow)),
            ('created_by', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['accounts.MDQUser'])),
            ('score', self.gf('django.db.models.fields.FloatField')()),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal(u'motsdits', ['Tag'])

        # Adding model 'Item'
        db.create_table(u'motsdits_item', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('approved', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('flags', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.utcnow)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.utcnow)),
            ('created_by', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['accounts.MDQUser'])),
            ('score', self.gf('django.db.models.fields.FloatField')()),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=5)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('address', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('lat', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('lng', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('website', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
        ))
        db.send_create_signal(u'motsdits', ['Item'])

        # Adding M2M table for field tags on 'Item'
        m2m_table_name = db.shorten_name(u'motsdits_item_tags')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('item', models.ForeignKey(orm[u'motsdits.item'], null=False)),
            ('tag', models.ForeignKey(orm[u'motsdits.tag'], null=False))
        ))
        db.create_unique(m2m_table_name, ['item_id', 'tag_id'])

        # Adding model 'MotDit'
        db.create_table(u'motsdits_motdit', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('approved', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('flags', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.utcnow)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.utcnow)),
            ('created_by', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['accounts.MDQUser'])),
            ('score', self.gf('django.db.models.fields.FloatField')()),
            ('action', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['motsdits.Action'])),
            ('what', self.gf('django.db.models.fields.related.ForeignKey')(related_name='what', to=orm['motsdits.Item'])),
            ('where', self.gf('django.db.models.fields.related.ForeignKey')(related_name='where', to=orm['motsdits.Item'])),
        ))
        db.send_create_signal(u'motsdits', ['MotDit'])


    def backwards(self, orm):
        # Deleting model 'Action'
        db.delete_table(u'motsdits_action')

        # Deleting model 'Tag'
        db.delete_table(u'motsdits_tag')

        # Deleting model 'Item'
        db.delete_table(u'motsdits_item')

        # Removing M2M table for field tags on 'Item'
        db.delete_table(db.shorten_name(u'motsdits_item_tags'))

        # Deleting model 'MotDit'
        db.delete_table(u'motsdits_motdit')


    models = {
        u'accounts.mdquser': {
            'Meta': {'object_name': 'MDQUser'},
            'date_of_birth': ('django.db.models.fields.DateField', [], {}),
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_admin': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        u'motsdits.action': {
            'Meta': {'object_name': 'Action'},
            'approved': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.utcnow'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['accounts.MDQUser']"}),
            'flags': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'score': ('django.db.models.fields.FloatField', [], {}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.utcnow'}),
            'verb': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'motsdits.item': {
            'Meta': {'object_name': 'Item'},
            'address': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'approved': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.utcnow'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['accounts.MDQUser']"}),
            'flags': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lat': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'lng': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'score': ('django.db.models.fields.FloatField', [], {}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['motsdits.Tag']", 'symmetrical': 'False'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.utcnow'}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        u'motsdits.motdit': {
            'Meta': {'object_name': 'MotDit'},
            'action': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['motsdits.Action']"}),
            'approved': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.utcnow'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['accounts.MDQUser']"}),
            'flags': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'score': ('django.db.models.fields.FloatField', [], {}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.utcnow'}),
            'what': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'what'", 'to': u"orm['motsdits.Item']"}),
            'where': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'where'", 'to': u"orm['motsdits.Item']"})
        },
        u'motsdits.tag': {
            'Meta': {'object_name': 'Tag'},
            'approved': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.utcnow'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['accounts.MDQUser']"}),
            'flags': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'score': ('django.db.models.fields.FloatField', [], {}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.utcnow'})
        }
    }

    complete_apps = ['motsdits']