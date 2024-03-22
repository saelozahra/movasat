from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views
urlpatterns = [
    path('', views.CoursePage.as_view(), name='CoursePage'),
    path('register/<cid>/<uid>', views.course_register, name='CourseRegister'),
    path('<cat>', views.course_view, name='CourseCatPage'),
    path('<cat>/<slug>', views.course_view, name='CourseView'),
    path('<cat>/<slug>/<lid>', views.lesson_view, name='LessonView'),
]