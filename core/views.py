from django.utils.timezone import now
from .models import AgoraNews, CourseAttendance, Courses, JoinCourse, User
from django.conf import settings

import requests
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
import uuid
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from .serializers import(
    AgoraNewsSerializer, CoursesSerializer, JoinCourseSerializer, JoinCourseCreateSerializer
)
from rest_framework import generics
from core.utils import get_tokens


def reCAPTCHA(token):
    data = {
        'secret': settings.RECAPTCHA_SECRET,
        'response': token
    }
    resp = requests.post(
        'https://www.google.com/recaptcha/api/siteverify',
        data=data
    )
    if not resp.json().get('success'):
        return False
    return True


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):

        username = request.data.get('username')
        password = request.data.get('password')
        g_token = request.data.get('gtoken')

        if username is None or password is None or g_token is None:
            return Response({
                "message": "invalid body"
            }, status=400)

        if not reCAPTCHA(request.data.get('gtoken', None)):
            return Response(data={'message': 'ReCAPTCHA not verified!'}, status=406)

        user = authenticate(username=username, password=password)
        if not user:
            return Response({"message": "Invalid Details"}, status=400)
        token, _ = Token.objects.get_or_create(user=user)
        return Response({
            "message": "User Logged In",
            "user": {
                "username": user.username,
                "full_name": user.full_name,
                "token": token.key,
                "user_type": user.user_type,
                "is_verified": user.is_verified
            }}, status=200)


class SignUp(APIView):
    permission_classes = [AllowAny]

    def post(self, request):

        username = request.data.get('username')
        password = request.data.get('password')
        full_name = request.data.get('full_name')
        g_token = request.data.get('gtoken')

        if username is None or password is None or g_token is None:
            return Response({
                "message": "invalid body"
            }, status=400)

        if not reCAPTCHA(request.data.get('gtoken', None)):
            return Response(data={'message': 'ReCAPTCHA not verified!'}, status=406)

        try:
            user = User.objects.create_user(
                username=username,
                password=password,
                full_name=full_name,
                user_type=0
            )
        except Exception as e:
            print(e)
            return Response(status=400)
        token, _ = Token.objects.get_or_create(user=user)
        return Response({
            "message": "User Logged In",
            "user": {
                "username": user.username,
                "full_name": user.full_name,
                "token": token.key,
                "user_type": user.user_type,
                "is_verified": user.is_verified
            }}, status=200)


class AgoraNewsAPI(generics.ListAPIView):
    queryset = AgoraNews.objects.all()
    serializer_class = AgoraNewsSerializer
    permission_classes = [IsAuthenticated]


class CoursesAPI(generics.ListAPIView):
    serializer_class = CoursesSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        registered_courses = JoinCourse.objects.filter(
            user=self.request.user).values_list('course', flat=True)
        return Courses.objects.exclude(id__in=registered_courses)


class RegisteredCoursesAPI(generics.ListCreateAPIView):
    serializer_class = JoinCourseSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == "POST":
            return JoinCourseCreateSerializer
        return JoinCourseSerializer

    def get_queryset(self):
        return JoinCourse.objects.filter(
            user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class JoinSession(APIView):
    def post(self, request):
        event_id = request.data.get('event_id')
        if event_id is None:
            return Response({
                "status": 400,
                "message": "Session not found"
            }, status=400)
        join_info = JoinCourse.objects.filter(id=event_id, user=request.user)
        if not join_info.exists():
            return Response({
                "status": 400,
                "message": "Session not found"
            }, status=400)
        join_info = join_info[0]
        if request.user.user_type == 0:
            if not join_info.course.is_live:
                return Response({
                    "status": 400,
                    "message": "Session not live"
                }, status=400)
        tokens = get_tokens(str(join_info.course.id),
                            request.user.user_type, request.user.username)
        # attendance = CourseAttendance(
        #     join_info=join_info, session_date=now(), is_present=True)
        # attendance.save()
        return Response(tokens, status=200)
