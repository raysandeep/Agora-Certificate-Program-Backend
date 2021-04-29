from django.contrib import admin

# Register your models here.
from . import models


admin.site.register(models.User)
admin.site.register(models.AgoraNews)
admin.site.register(models.Courses)
admin.site.register(models.JoinCourse)
