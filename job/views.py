from django.shortcuts import render
from .models import *


def all_job(request):
    get_jobs = Job.objects.all()
    return render(request, "", context={'data': get_jobs})


def job(request, jowner, jcat, jid):
    j1 = Job.objects.filter(id=jid).get()
    return render(request, "JobSingle.html", context={
        'job': j1,
        "edit_url": j1.get_edit_url(),
    })
