from django.shortcuts import render
from .models import *


def job(request):
    get_jobs = Job.objects.all()
    return render(request, "", context={'data': get_jobs})
