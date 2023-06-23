from django.shortcuts import render
from .models import *


def all_job(request):
    get_jobs = Job.objects.all()
    return render(request, "", context={'data': get_jobs})


def job(request, jowner, jid):
    job = Job.objects.filter(id=jid).get()
    return render(request, "JobSingle.html", context={'job': job})
