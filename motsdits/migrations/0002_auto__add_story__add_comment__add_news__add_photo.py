# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Story'
        db.create_table(u'motsdits_story', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('approved', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('flags', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.utcnow)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.utcnow)),
            ('created_by', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['accounts.MDQUser'])),
            ('score', self.gf('django.db.models.fields.FloatField')(default=0)),
            ('text', self.gf('django.db.models.fields.TextField')()),
            ('motdit', self.gf('django.db.models.fields.related.ForeignKey')(related_name='stories', to=orm['motsdits.MotDit'])),
        ))
        db.send_create_signal(u'motsdits', ['Story'])

        # Adding model 'Comment'
        db.create_table(u'motsdits_comment', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('approved', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('flags', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.utcnow)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.utcnow)),
            ('created_by', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['accounts.MDQUser'])),
            ('score', self.gf('django.db.models.fields.FloatField')(default=0)),
            ('text', self.gf('django.db.models.fields.TextField')()),
            ('news_item', self.gf('django.db.models.fields.related.ForeignKey')(related_name='comments', to=orm['motsdits.News'])),
        ))
        db.send_create_signal(u'motsdits', ['Comment'])

        # Adding model 'News'
        db.create_table(u'motsdits_news', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('approved', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('flags', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.utcnow)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.utcnow)),
            ('created_by', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['accounts.MDQUser'])),
            ('score', self.gf('django.db.models.fields.FloatField')(default=0)),
            ('motdit', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['motsdits.MotDit'])),
            ('photo', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['motsdits.Photo'], null=True, blank=True)),
            ('story', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['motsdits.Story'], null=True, blank=True)),
        ))
        db.send_create_signal(u'motsdits', ['News'])

        # Adding model 'Photo'
        db.create_table(u'motsdits_photo', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('approved', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('flags', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.utcnow)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.utcnow)),
            ('created_by', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['accounts.MDQUser'])),
            ('score', self.gf('django.db.models.fields.FloatField')(default=0)),
            ('picture', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
            ('motdit', self.gf('django.db.models.fields.related.ForeignKey')(related_name='photos', to=orm['motsdits.MotDit'])),
        ))
        db.send_create_signal(u'motsdits', ['Photo'])


    def backwards(self, orm):
        # Deleting model 'Story'
        db.delete_table(u'motsdits_story')

        # Deleting model 'Comment'
        db.delete_table(u'motsdits_comment')

        # Deleting model 'News'
        db.delete_table(u'motsdits_news')

        # Deleting model 'Photo'
        db.delete_table(u'motsdits_photo')


    models = {
        u'accounts.mdquser': {
            'Meta': {'object_name': 'MDQUser'},
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '255'}),
            'favourites': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'favourites'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['motsdits.MotDit']"}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_admin': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'likes': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'likes'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['motsdits.MotDit']"}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        u'motsdits.action': {
            'Meta': {'object_name': 'Action'},
            'approved': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.utcnow'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['accounts.MDQUser']"}),
            'flags': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'score': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.utcnow'}),
            'verb': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'motsdits.comment': {
            'Meta': {'object_name': 'Comment'},
            'approved': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.utcnow'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['accounts.MDQUser']"}),
            'flags': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'news_item': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'comments'", 'to': u"orm['motsdits.News']"}),
            'score': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'text': ('django.db.models.fields.TextField', [], {}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.utcnow'})
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
            'score': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['motsdits.Tag']", 'null': 'True', 'blank': 'True'}),
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
            'score': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.utcnow'}),
            'what': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'what'", 'to': u"orm['motsdits.Item']"}),
            'where': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'where'", 'to': u"orm['motsdits.Item']"})
        },
        u'motsdits.news': {
            'Meta': {'object_name': 'News'},
            'approved': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.utcnow'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['accounts.MDQUser']"}),
            'flags': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'motdit': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['motsdits.MotDit']"}),
            'photo': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['motsdits.Photo']", 'null': 'True', 'blank': 'True'}),
            'score': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'story': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['motsdits.Story']", 'null': 'True', 'blank': 'True'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.utcnow'})
        },
        u'motsdits.photo': {
            'Meta': {'object_name': 'Photo'},
            'approved': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.utcnow'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['accounts.MDQUser']"}),
            'flags': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'motdit': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'photos'", 'to': u"orm['motsdits.MotDit']"}),
            'picture': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'score': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.utcnow'})
        },
        u'motsdits.story': {
            'Meta': {'object_name': 'Story'},
            'approved': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.utcnow'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['accounts.MDQUser']"}),
            'flags': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'motdit': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'stories'", 'to': u"orm['motsdits.MotDit']"}),
            'score': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'text': ('django.db.models.fields.TextField', [], {}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.utcnow'})
        },
        u'motsdits.tag': {
            'Meta': {'object_name': 'Tag'},
            'approved': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.utcnow'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['accounts.MDQUser']"}),
            'flags': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'score': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.utcnow'})
        }
    }

    complete_apps = ['motsdits']