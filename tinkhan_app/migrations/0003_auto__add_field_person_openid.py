# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Person.openid'
        db.add_column('tinkhan_app_person', 'openid',
                      self.gf('django.db.models.fields.URLField')(default='', max_length=200, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Person.openid'
        db.delete_column('tinkhan_app_person', 'openid')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
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
            'khan_id': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '255'}),
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
            'khan_id': ('django.db.models.fields.IntegerField', [], {'unique': 'True', 'db_index': 'True'}),
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
            'khan_id': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '255'}),
            'live': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'prerequisites': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'leads_to+'", 'symmetrical': 'False', 'to': "orm['khan.Exercise']"}),
            'seconds_per_fast_problem': ('django.db.models.fields.FloatField', [], {}),
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
            'first_done': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_done': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'last_review': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'longest_streak': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'proficient_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'seconds_per_fast_problem': ('django.db.models.fields.FloatField', [], {}),
            'streak': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'summative': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
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
            'khan_id': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '255'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'subtopics'", 'null': 'True', 'blank': 'True', 'to': "orm['khan.Topic']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        },
        'khan.userdata': {
            'Meta': {'object_name': 'UserData'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'earned_badges': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['khan.Badge']", 'through': "orm['khan.BadgeEarn']", 'symmetrical': 'False'}),
            'exercise_performances': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['khan.Exercise']", 'through': "orm['khan.Performance']", 'symmetrical': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'joined': ('django.db.models.fields.DateTimeField', [], {}),
            'last_activity': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'nickname': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'points': ('django.db.models.fields.IntegerField', [], {}),
            'prettified_user_email': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'proficient_exercises': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'proficient_users'", 'symmetrical': 'False', 'to': "orm['khan.Exercise']"}),
            'suggested_exercises': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'+'", 'symmetrical': 'False', 'to': "orm['khan.Exercise']"}),
            'total_seconds_watched': ('django.db.models.fields.IntegerField', [], {}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'user_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255', 'db_index': 'True'}),
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
            'khan_id': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '255'}),
            'position': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'topic': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'videos'", 'null': 'True', 'to': "orm['khan.Topic']"}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'views': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'youtube_id': ('django.db.models.fields.CharField', [], {'max_length': '32'})
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
        },
        'tincan_exporter.tincanendpoint': {
            'Meta': {'object_name': 'TinCanEndpoint'},
            'auth_type': ('django.db.models.fields.CharField', [], {'default': "'b'", 'max_length': '1'}),
            'hostname': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'path': ('django.db.models.fields.CharField', [], {'default': "'/TCAPI/statements'", 'max_length': '255'}),
            'ssl': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'tincan_endpoints'", 'to': "orm['auth.User']"}),
            'username': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'})
        },
        'tinkhan_app.person': {
            'Meta': {'object_name': 'Person'},
            'account': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tinkhan_app.UserProfile']"}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'openid': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'tc_account_homePage': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'tc_account_id': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'use_tc_account': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'userdata': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['khan.UserData']", 'null': 'True', 'blank': 'True'})
        },
        'tinkhan_app.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'company': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'tcapi_endpoint': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['tincan_exporter.TinCanEndpoint']", 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True'})
        }
    }

    complete_apps = ['tinkhan_app']