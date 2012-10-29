# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'FetchData'
        db.create_table('khan_fetchdata', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('khan', ['FetchData'])

        # Adding model 'Topic'
        db.create_table('khan_topic', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, auto_now_add=True, blank=True)),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(related_name='subtopics', to=orm['khan.Topic'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('khan_id', self.gf('django.db.models.fields.SlugField')(max_length=50)),
        ))
        db.send_create_signal('khan', ['Topic'])

        # Adding model 'VideoSource'
        db.create_table('khan_videosource', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, auto_now_add=True, blank=True)),
            ('format', self.gf('django.db.models.fields.CharField')(max_length=8)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('video', self.gf('django.db.models.fields.related.ForeignKey')(related_name='sources', to=orm['khan.Video'])),
        ))
        db.send_create_signal('khan', ['VideoSource'])

        # Adding model 'Video'
        db.create_table('khan_video', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, auto_now_add=True, blank=True)),
            ('topic', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='videos', null=True, to=orm['khan.Topic'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('position', self.gf('django.db.models.fields.IntegerField')()),
            ('keywords', self.gf('django.db.models.fields.TextField')()),
            ('duration', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('khan_id', self.gf('django.db.models.fields.SlugField')(max_length=50)),
            ('youtube_id', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('views', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('date_added', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal('khan', ['Video'])

        # Adding model 'Exercise'
        db.create_table('khan_exercise', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, auto_now_add=True, blank=True)),
            ('topic', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='exercises', null=True, to=orm['khan.Topic'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('short_name', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('live', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('summative', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('khan_id', self.gf('django.db.models.fields.SlugField')(max_length=50)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('h_position', self.gf('django.db.models.fields.IntegerField')()),
            ('v_position', self.gf('django.db.models.fields.IntegerField')()),
            ('seconds_per_fast_problem', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('khan', ['Exercise'])

        # Adding M2M table for field prerequisites on 'Exercise'
        db.create_table('khan_exercise_prerequisites', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('from_exercise', models.ForeignKey(orm['khan.exercise'], null=False)),
            ('to_exercise', models.ForeignKey(orm['khan.exercise'], null=False))
        ))
        db.create_unique('khan_exercise_prerequisites', ['from_exercise_id', 'to_exercise_id'])

        # Adding model 'BadgeCategory'
        db.create_table('khan_badgecategory', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, auto_now_add=True, blank=True)),
            ('khan_id', self.gf('django.db.models.fields.IntegerField')()),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('type_label', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('chart_icon_src', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('icon_src', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('large_icon_src', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('khan', ['BadgeCategory'])

        # Adding model 'Badge'
        db.create_table('khan_badge', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, auto_now_add=True, blank=True)),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['khan.BadgeCategory'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('khan_id', self.gf('django.db.models.fields.SlugField')(max_length=50)),
            ('points', self.gf('django.db.models.fields.PositiveIntegerField')()),
        ))
        db.send_create_signal('khan', ['Badge'])

        # Adding model 'BadgeEarn'
        db.create_table('khan_badgeearn', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, auto_now_add=True, blank=True)),
            ('badge', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['khan.Badge'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['khan.UserData'])),
            ('date_earned', self.gf('django.db.models.fields.DateTimeField')()),
            ('points_earned', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('target_context_content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'])),
            ('target_context_object_id', self.gf('django.db.models.fields.IntegerField')()),
            ('target_context_name', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('khan', ['BadgeEarn'])

        # Adding model 'Performance'
        db.create_table('khan_performance', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, auto_now_add=True, blank=True)),
            ('exercise', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['khan.Exercise'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['khan.UserData'])),
            ('first_done', self.gf('django.db.models.fields.DateTimeField')()),
            ('last_done', self.gf('django.db.models.fields.DateTimeField')()),
            ('last_review', self.gf('django.db.models.fields.DateTimeField')()),
            ('longest_streak', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('proficient_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('streak', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('total_done', self.gf('django.db.models.fields.PositiveIntegerField')()),
        ))
        db.send_create_signal('khan', ['Performance'])

        # Adding model 'Watch'
        db.create_table('khan_watch', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, auto_now_add=True, blank=True)),
            ('video', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['khan.Video'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['khan.UserData'])),
            ('completed', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('last_second_watched', self.gf('django.db.models.fields.IntegerField')()),
            ('last_watched', self.gf('django.db.models.fields.DateTimeField')()),
            ('points', self.gf('django.db.models.fields.IntegerField')()),
            ('seconds_watched', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('khan', ['Watch'])

        # Adding model 'UserData'
        db.create_table('khan_userdata', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, auto_now_add=True, blank=True)),
            ('nickname', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('user_id', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('prettified_user_email', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('joined', self.gf('django.db.models.fields.DateTimeField')()),
            ('last_activity', self.gf('django.db.models.fields.DateTimeField')()),
            ('points', self.gf('django.db.models.fields.IntegerField')()),
            ('total_seconds_watched', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('khan', ['UserData'])

        # Adding M2M table for field proficient_exercises on 'UserData'
        db.create_table('khan_userdata_proficient_exercises', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('userdata', models.ForeignKey(orm['khan.userdata'], null=False)),
            ('exercise', models.ForeignKey(orm['khan.exercise'], null=False))
        ))
        db.create_unique('khan_userdata_proficient_exercises', ['userdata_id', 'exercise_id'])

        # Adding M2M table for field suggested_exercises on 'UserData'
        db.create_table('khan_userdata_suggested_exercises', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('userdata', models.ForeignKey(orm['khan.userdata'], null=False)),
            ('exercise', models.ForeignKey(orm['khan.exercise'], null=False))
        ))
        db.create_unique('khan_userdata_suggested_exercises', ['userdata_id', 'exercise_id'])


    def backwards(self, orm):
        # Deleting model 'FetchData'
        db.delete_table('khan_fetchdata')

        # Deleting model 'Topic'
        db.delete_table('khan_topic')

        # Deleting model 'VideoSource'
        db.delete_table('khan_videosource')

        # Deleting model 'Video'
        db.delete_table('khan_video')

        # Deleting model 'Exercise'
        db.delete_table('khan_exercise')

        # Removing M2M table for field prerequisites on 'Exercise'
        db.delete_table('khan_exercise_prerequisites')

        # Deleting model 'BadgeCategory'
        db.delete_table('khan_badgecategory')

        # Deleting model 'Badge'
        db.delete_table('khan_badge')

        # Deleting model 'BadgeEarn'
        db.delete_table('khan_badgeearn')

        # Deleting model 'Performance'
        db.delete_table('khan_performance')

        # Deleting model 'Watch'
        db.delete_table('khan_watch')

        # Deleting model 'UserData'
        db.delete_table('khan_userdata')

        # Removing M2M table for field proficient_exercises on 'UserData'
        db.delete_table('khan_userdata_proficient_exercises')

        # Removing M2M table for field suggested_exercises on 'UserData'
        db.delete_table('khan_userdata_suggested_exercises')


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
            'target_context_content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'target_context_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'target_context_object_id': ('django.db.models.fields.IntegerField', [], {}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['khan.UserData']"})
        },
        'khan.exercise': {
            'Meta': {'object_name': 'Exercise'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'h_position': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'khan_id': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'live': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'prerequisites': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['khan.Exercise']", 'symmetrical': 'False'}),
            'seconds_per_fast_problem': ('django.db.models.fields.IntegerField', [], {}),
            'short_name': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'summative': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'topic': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'exercises'", 'null': 'True', 'to': "orm['khan.Topic']"}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'v_position': ('django.db.models.fields.IntegerField', [], {})
        },
        'khan.fetchdata': {
            'Meta': {'object_name': 'FetchData'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'})
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
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'subtopics'", 'to': "orm['khan.Topic']"}),
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
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['khan.UserData']"}),
            'video': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['khan.Video']"})
        }
    }

    complete_apps = ['khan']