from django.urls import path
from .views import *

urlpatterns = [
    path('all_job', job, name="all_job"),
]