from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views
urlpatterns = [
    path('course', views.CoursePage.as_view(), name='CoursePage'),
    path('course/<cat>', views.course_view, name='CourseCatPage'),
    path('course/<cat>/<slug>', views.course_view, name='CourseView'),
    path('course/<cat>/<slug>/<lid>', views.lesson_view, name='LessonView'),
]