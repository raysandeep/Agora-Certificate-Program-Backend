from django.db.models import fields
from rest_framework import serializers
from .models import AgoraNews, Courses, JoinCourse


class AgoraNewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AgoraNews
        fields = '__all__'


class CoursesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Courses
        fields = '__all__'


class JoinCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = JoinCourse
        exclude = ['user']
        depth = 1


class JoinCourseCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = JoinCourse
        exclude = ['is_completed', 'user']
