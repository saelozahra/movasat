from django.urls import path
from .views import *

urlpatterns = [
    path('job', all_job, name="all_job"),
    path('job/<jcat>', job, name='job_cat'),
    path('job/<jowner>/<jcat>/<jid>', job, name='single_job'),
]