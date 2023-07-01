from django.shortcuts import render, redirect
from django.views.generic import CreateView
from job.forms import RegisterJob

from .models import *


def all_job(request):
    get_jobs = Job.objects.all()
    return render(request, "JobPage.html", context={'jobs': get_jobs})


def job_cat(request, jcat):
    get_jobs = Job.objects.filter(JobCat__slug=jcat).all()
    return render(request, "JobPage.html", context={'jobs': get_jobs})


def job(request, jowner, jcat, jid):
    j1 = Job.objects.filter(id=jid).get()
    return render(request, "JobSingle.html", context={
        'job': j1,
        "edit_url": j1.get_edit_url(),
    })


class JobCreate(CreateView):
    form_class = RegisterJob
    template_name = "JobRegister.html"

    def form_valid(self, form):
        j = form.save(commit=False)
        j.owner = self.request.user.id
        j.save()
        return redirect("all_job")

