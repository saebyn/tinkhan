# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'FetchData'
        db.delete_table('khan_fetchdata')

        # Adding field 'Watch.synchronized'
        db.add_column('khan_watch', 'synchronized',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'Performance.synchronized'
        db.add_column('khan_performance', 'synchronized',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'BadgeEarn.synchronized'
        db.add_column('khan_badgeearn', 'synchronized',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)


    def backwards(self, orm):
        # Adding model 'FetchData'
        db.create_table('khan_fetchdata', (
            ('updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, auto_now_add=True, blank=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('khan', ['FetchData'])

        # Deleting field 'Watch.synchronized'
        db.delete_column('khan_watch', 'synchronized')

        # Deleting field 'Performance.synchronized'
        db.delete_column('khan_performance', 'synchronized')

        # Deleting field 'BadgeEarn.synchronized'
        db.delete_column('khan_badgeearn', 'synchronized')


    models = {
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'khan.badge': {
            'Meta': {'object_name': 'Badge'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['khan.BadgeCategory']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'khan_id': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'points': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'})
        },
        'khan.badgecategory': {
            'Meta': {'object_name': 'BadgeCategory'},
            'chart_icon_src': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'icon_src': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'khan_id': ('django.db.models.fields.IntegerField', [], {}),
            'large_icon_src': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'type_label': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'})
        },
        'khan.badgeearn': {
            'Meta': {'object_name': 'BadgeEarn'},
            'badge': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['khan.Badge']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_earned': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'points_earned': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'synchronized': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'target_context_content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'target_context_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'target_context_object_id': ('django.db.models.fields.IntegerField', [], {}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['khan.UserData']"})
        },
        'khan.exercise': {
            'Meta': {'object_name': 'Exercise'},
            'covers': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'covered_by+'", 'symmetrical': 'False', 'to': "orm['khan.Exercise']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'h_position': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'khan_id': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'live': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'prerequisites': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'leads_to+'", 'symmetrical': 'False', 'to': "orm['khan.Exercise']"}),
            'seconds_per_fast_problem': ('django.db.models.fields.IntegerField', [], {}),
            'short_name': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'summative': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'topic': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'exercises'", 'null': 'True', 'to': "orm['khan.Topic']"}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'v_position': ('django.db.models.fields.IntegerField', [], {})
        },
        'khan.performance': {
            'Meta': {'object_name': 'Performance'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'exercise': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['khan.Exercise']"}),
            'first_done': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_done': ('django.db.models.fields.DateTimeField', [], {}),
            'last_review': ('django.db.models.fields.DateTimeField', [], {}),
            'longest_streak': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'proficient_date': ('django.db.models.fields.DateTimeField', [], {}),
            'streak': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'synchronized': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'total_done': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['khan.UserData']"})
        },
        'khan.topic': {
            'Meta': {'object_name': 'Topic'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'khan_id': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'subtopics'", 'null': 'True', 'blank': 'True', 'to': "orm['khan.Topic']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'})
        },
        'khan.userdata': {
            'Meta': {'object_name': 'UserData'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'earned_badges': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['khan.Badge']", 'through': "orm['khan.BadgeEarn']", 'symmetrical': 'False'}),
            'exercise_performances': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['khan.Exercise']", 'through': "orm['khan.Performance']", 'symmetrical': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'joined': ('django.db.models.fields.DateTimeField', [], {}),
            'last_activity': ('django.db.models.fields.DateTimeField', [], {}),
            'nickname': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'points': ('django.db.models.fields.IntegerField', [], {}),
            'prettified_user_email': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'proficient_exercises': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'proficient_users'", 'symmetrical': 'False', 'to': "orm['khan.Exercise']"}),
            'suggested_exercises': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'+'", 'symmetrical': 'False', 'to': "orm['khan.Exercise']"}),
            'total_seconds_watched': ('django.db.models.fields.IntegerField', [], {}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'user_id': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'watched_videos': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['khan.Video']", 'through': "orm['khan.Watch']", 'symmetrical': 'False'})
        },
        'khan.video': {
            'Meta': {'object_name': 'Video'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_added': ('django.db.models.fields.DateTimeField', [], {}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'duration': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'keywords': ('django.db.models.fields.TextField', [], {}),
            'khan_id': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'position': ('django.db.models.fields.IntegerField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'topic': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'videos'", 'null': 'True', 'to': "orm['khan.Topic']"}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'views': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'youtube_id': ('django.db.models.fields.CharField', [], {'max_length': '32'})
        },
        'khan.videosource': {
            'Meta': {'object_name': 'VideoSource'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'format': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'video': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'sources'", 'to': "orm['khan.Video']"})
        },
        'khan.watch': {
            'Meta': {'object_name': 'Watch'},
            'completed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_second_watched': ('django.db.models.fields.IntegerField', [], {}),
            'last_watched': ('django.db.models.fields.DateTimeField', [], {}),
            'points': ('django.db.models.fields.IntegerField', [], {}),
            'seconds_watched': ('django.db.models.fields.IntegerField', [], {}),
            'synchronized': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['khan.UserData']"}),
            'video': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['khan.Video']"})
        }
    }

    complete_apps = ['khan']