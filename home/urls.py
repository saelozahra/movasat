from django.urls import path
from lms import views

urlpatterns = [
    path(r'', views.CoursePage.as_view(), name="index"),
]