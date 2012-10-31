# vim: set fileencoding=utf-8 ft=python ff=unix nowrap tabstop=4 shiftwidth=4 softtabstop=4 smarttab shiftround expandtab :
from django.contrib import admin

from khan.models import Topic, Video, VideoSource, Exercise, BadgeCategory,\
        Badge, BadgeEarn, Performance, Watch, UserData


# TODO add better admin

admin.site.register(Topic)
admin.site.register(Video)
admin.site.register(VideoSource)
admin.site.register(Exercise)
admin.site.register(BadgeCategory)
admin.site.register(Badge)
admin.site.register(BadgeEarn)
admin.site.register(Performance)
admin.site.register(Watch)
admin.site.register(UserData)
