# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'News.motdit'
        db.alter_column(u'motsdits_news', 'motdit_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['motsdits.MotDit'], null=True))

    def backwards(self, orm):

        # User chose to not deal with backwards NULL issues for 'News.motdit'
        raise RuntimeError("Cannot reverse this migration. 'News.motdit' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration
        # Changing field 'News.motdit'
        db.alter_column(u'motsdits_news', 'motdit_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['motsdits.MotDit']))

    models = {
        u'accounts.mdquser': {
            'Meta': {'object_name': 'MDQUser'},
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '255'}),
            'favourites': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'favourites'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['motsdits.MotDit']"}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'following': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'followers'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['accounts.MDQUser']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_admin': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'liked_photos': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'likes'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['motsdits.Photo']"}),
            'liked_stories': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'likes'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['motsdits.Story']"}),
            'likes': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'likes'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['motsdits.MotDit']"}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'validated': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'validation_code': ('django.db.models.fields.CharField', [], {'default': "'b86d960d23d240cca90060c3256134b4'", 'max_length': '255', 'null': 'True', 'blank': 'True'})
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
            'verb': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        u'motsdits.answer': {
            'Meta': {'object_name': 'Answer'},
            'answer': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'answer_to'", 'to': u"orm['motsdits.MotDit']"}),
            'approved': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.utcnow'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['accounts.MDQUser']"}),
            'flags': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'answers'", 'to': u"orm['motsdits.Question']"}),
            'score': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.utcnow'})
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
            'what': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'what'", 'null': 'True', 'to': u"orm['motsdits.Item']"}),
            'where': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'where'", 'null': 'True', 'to': u"orm['motsdits.Item']"})
        },
        u'motsdits.news': {
            'Meta': {'object_name': 'News'},
            'action': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'answer': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'news_about'", 'null': 'True', 'to': u"orm['motsdits.Answer']"}),
            'approved': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.utcnow'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['accounts.MDQUser']"}),
            'flags': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'motdit': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['motsdits.MotDit']", 'null': 'True', 'blank': 'True'}),
            'photo': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['motsdits.Photo']", 'null': 'True', 'blank': 'True'}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'news_about'", 'null': 'True', 'to': u"orm['motsdits.Question']"}),
            'score': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'story': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['motsdits.Story']", 'null': 'True', 'blank': 'True'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.utcnow'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'news_about'", 'null': 'True', 'to': u"orm['accounts.MDQUser']"})
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
        u'motsdits.question': {
            'Meta': {'object_name': 'Question', '_ormbases': [u'motsdits.MotDit']},
            u'motdit_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['motsdits.MotDit']", 'unique': 'True', 'primary_key': 'True'})
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