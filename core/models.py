from django.db import models
import uuid
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class MyUserManager(BaseUserManager):

    def create_user(self, username, full_name, user_type, password):
        if not username:
            raise ValueError('Users must have an email address')
        if not full_name:
            raise ValueError('Users must have a full name')
        if not user_type:
            # By default normal user
            user_type = 0
        if not password:
            raise ValueError('Password Required')
        elif len(password) < 6:
            raise ValueError('Password should be atleast 6 char')

        user = self.model(
            username=self.normalize_email(username),
            full_name=full_name,
            user_type=user_type
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, full_name, password):
        user = self.create_user(
            username=self.normalize_email(username),
            full_name=full_name,
            user_type=2,
            password=password
        )
        user.set_password(password)
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    username = models.EmailField(
        verbose_name="username", max_length=253, unique=True)
    full_name = models.CharField(verbose_name="fullname", max_length=60)
    # normal user - 0, retailer - 1, admin - 2, company - 3
    user_type = models.IntegerField(editable=False)
    date_joined = models.DateTimeField(
        verbose_name='date joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_blocked = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['full_name']

    objects = MyUserManager()

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True


class AgoraNews(models.Model):
    title = models.CharField(max_length=256)
    description = models.TextField()
    tags = models.CharField(max_length=256)
    links = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)
    url = models.URLField(null=True)


class Courses(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    name = models.CharField(max_length=256)
    description = models.TextField()
    tags = models.CharField(max_length=256)
    capacity = models.IntegerField(default=500)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    session_timings = models.JSONField(default=dict)
    url = models.URLField(null=True)
    is_live = models.BooleanField(default=False)


class JoinCourse(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    course = models.ForeignKey(Courses, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    joined_date = models.DateTimeField(auto_now_add=True)
    is_completed = models.BooleanField(default=False)


class CourseAttendance(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    join_info = models.ForeignKey(JoinCourse, on_delete=models.CASCADE)
    session_date = models.DateTimeField()
    is_present = models.BooleanField(default=False)
