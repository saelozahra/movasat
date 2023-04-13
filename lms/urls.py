from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views
urlpatterns = [
    path('course', views.CoursePage.as_view(), name='CoursePage'),
    path('course/lesson/<slug>', views.course_view, name='LessonView'),
]