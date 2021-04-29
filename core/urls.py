from django.urls import path
from . import views


urlpatterns = [
    path('login/', views.LoginView.as_view()),
    path('signup/', views.SignUp.as_view()),
    path('news/', views.AgoraNewsAPI.as_view()),
    path('available/courses/', views.CoursesAPI.as_view()),
    path('registered/courses/', views.RegisteredCoursesAPI.as_view()),
    path('join/session/', views.JoinSession.as_view())
]
