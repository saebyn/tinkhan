# vim: set fileencoding=utf-8 ft=python ff=unix nowrap tabstop=4 shiftwidth=4 softtabstop=4 smarttab shiftround expandtab :
"""
Models for the `khan` Django app.
"""

from django.db import models

from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

from khan.managers import TopicManager, UserDataManager, ExerciseManager,\
        VideoManager, BadgeManager


class BaseModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=True)

    class Meta:
        abstract = True


class UserActivityModelMixin(models.Model):
    synchronized = models.BooleanField(default=False)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.synchronized = False
        return super(UserActivityModelMixin, self).save(*args, **kwargs)

    def synchronize(self):
        self.synchronized = True
        return models.Model.save(self)


class Topic(BaseModel):
    parent = models.ForeignKey('self', related_name='subtopics', null=True,
            blank=True, default=None)
    title = models.CharField(max_length=255)
    description = models.TextField()
    khan_id = models.SlugField(max_length=255, unique=True)
    url = models.URLField()

    objects = TopicManager()

    def __unicode__(self):
        return self.title


class VideoSource(BaseModel):
    format = models.CharField(max_length=8)
    url = models.URLField()
    video = models.ForeignKey('Video', related_name='sources')


class Video(BaseModel):
    topic = models.ForeignKey(Topic, null=True, blank=True, related_name='videos')
    title = models.CharField(max_length=255)
    description = models.TextField()
    position = models.IntegerField(null=True, blank=True)
    keywords = models.TextField()
    # duration in seconds
    duration = models.PositiveIntegerField()
    # `ka_url` - the khan academy URL for the video
    url = models.URLField()
    # `readable_id`
    khan_id = models.SlugField(max_length=255, unique=True)
    youtube_id = models.CharField(max_length=32)
    views = models.PositiveIntegerField()
    # `date_added` - When the video was added to Khan Academy
    date_added = models.DateTimeField()

    objects = VideoManager()

    def __unicode__(self):
        return self.title


class Exercise(BaseModel):
    topic = models.ForeignKey(Topic, null=True, blank=True, related_name='exercises')
    name = models.CharField(max_length=255)
    short_name = models.CharField(max_length=32)
    description = models.TextField()
    live = models.BooleanField()
    summative = models.BooleanField()
    # `name`
    khan_id = models.SlugField(max_length=255, unique=True)
    # `ka_url`
    url = models.URLField()
    prerequisites = models.ManyToManyField('self', symmetrical=False, related_name='leads_to+')
    covers = models.ManyToManyField('self', symmetrical=False, related_name='covered_by+')
    h_position = models.IntegerField()
    v_position = models.IntegerField()
    seconds_per_fast_problem = models.FloatField()

    objects = ExerciseManager()

    def __unicode__(self):
        return self.name


class BadgeCategory(BaseModel):
    # `category` identifier
    khan_id = models.IntegerField(unique=True, db_index=True)
    description = models.TextField()
    type_label = models.CharField(max_length=255)

    chart_icon_src = models.CharField(max_length=255)
    icon_src = models.CharField(max_length=255)
    large_icon_src = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = 'badge categories'


class Badge(BaseModel):
    category = models.ForeignKey(BadgeCategory)
    # `description`
    name = models.CharField(max_length=255)
    # `safe_extended_description`
    description = models.TextField()
    # `name`
    khan_id = models.SlugField(max_length=255, unique=True)
    points = models.PositiveIntegerField()

    objects = BadgeManager()


class BadgeEarn(UserActivityModelMixin, BaseModel):
    """
    This is the `through` model for our m2m relation between
    a user's UserData and a Badge.
    """
    badge = models.ForeignKey(Badge)
    user = models.ForeignKey('UserData')

    # `date`
    date_earned = models.DateTimeField()
    points_earned = models.PositiveIntegerField()

    target_context_content_type = models.ForeignKey(ContentType, null=True, blank=True)
    target_context_object_id = models.IntegerField(null=True, blank=True)
    target_context = generic.GenericForeignKey(
            'target_context_content_type', 'target_context_object_id')

    target_context_name = models.CharField(max_length=255)


class Performance(UserActivityModelMixin, BaseModel):
    """
    This is the `through` model for our m2m relation between
    a user's UserData and an Exercise.
    """
    exercise = models.ForeignKey(Exercise)
    user = models.ForeignKey('UserData')
    first_done = models.DateTimeField(null=True, blank=True)
    last_done = models.DateTimeField(null=True, blank=True)
    last_review = models.DateTimeField(null=True, blank=True)
    longest_streak = models.PositiveIntegerField()
    proficient_date = models.DateTimeField(null=True, blank=True)
    streak = models.PositiveIntegerField()
    total_done = models.PositiveIntegerField()
    summative = models.BooleanField()
    seconds_per_fast_problem = models.FloatField()


class Watch(UserActivityModelMixin, BaseModel):
    """
    This is the `through` model for our m2m relation between
    a user's UserData and a Video.
    """
    video = models.ForeignKey(Video)
    user = models.ForeignKey('UserData')
    completed = models.BooleanField()
    last_second_watched = models.IntegerField()
    last_watched = models.DateTimeField()
    points = models.IntegerField()
    seconds_watched = models.IntegerField()

    class Meta:
        verbose_name_plural = 'watches'


class UserData(BaseModel):
    nickname = models.CharField(max_length=255)
    user_id = models.CharField(max_length=255, unique=True, db_index=True)
    prettified_user_email = models.CharField(max_length=255)
    joined = models.DateTimeField()
    last_activity = models.DateTimeField(null=True, blank=True)
    points = models.IntegerField()
    total_seconds_watched = models.IntegerField()

    proficient_exercises = models.ManyToManyField(Exercise, related_name='proficient_users')
    suggested_exercises = models.ManyToManyField(Exercise, related_name='+')

    watched_videos = models.ManyToManyField(Video, through=Watch)
    exercise_performances = models.ManyToManyField(Exercise, through=Performance)
    earned_badges = models.ManyToManyField(Badge, through=BadgeEarn)

    objects = UserDataManager()

    class Meta:
        verbose_name = 'user datum'
        verbose_name_plural = 'user data'
