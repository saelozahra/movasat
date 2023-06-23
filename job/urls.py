from django.urls import path
from .views import *

urlpatterns = [
    path('job', all_job, name="all_job"),
    path('job/<jowner>/<jid>', job, name='single_job'),
]