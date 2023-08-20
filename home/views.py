import madadyar.models
from challenge.models import Forum, Divar
from harkat.models import CrowdFunding, Project
from job.models import Job
from lms.models import Course
from madadyar.models import JahadActivity
from django.shortcuts import render

# Create your views here.


def home_view(request):
    projects_data = []
    for jad in JahadActivity.objects.all():
        projects_data.append({
            'id': jad.id,
            'title': jad.title,
            'lat': jad.location.split(",")[0],
            'lng': jad.location.split(",")[1],
            'photo': jad.MadadKar.Avatar.url,
            'icon': jad.MadadKar.Avatar.url,
            # 'icon': "https://cdn4.iconfinder.com/data/icons/charity-and-donation-10/64/Untitled-1-05-64.png",
            'type': "JahadActivity",
            'date': jad.MadadJoo.RegisterDate,
            'url': jad.MadadKar.get_absolute_url(),#@todo jad.get_absolute_url,
        })

    for cd in CrowdFunding.objects.exclude(Location="").all():
        projects_data.append({
            'id': cd.id,
            'title': cd.Title,
            'lat': cd.Location.split(",")[0],
            'lng': cd.Location.split(",")[1],
            'photo': cd.Picture.url,
            'icon': "https://cdn1.iconfinder.com/data/icons/business-people-55/85/man_businessman_location_pin_gps_marker-128.png",
            'type': "CrowdFunding",
            'date': cd.date,
            'url': cd.get_absolute_url(),
        })


    for pd in Project.objects.exclude(location="").all():
        projects_data.append({
            'id': pd.id,
            'title': pd.name,
            'lat': pd.location.split(",")[0],
            'lng': pd.location.split(",")[1],
            'photo': pd.thumbnail.url,
            'icon': "https://cdn0.iconfinder.com/data/icons/task-and-project-management-19/512/Location__Marker__Pin__Pointer-128.png",
            'type': "Project",
            'date': pd.date,
            'url': pd.madadkar.get_absolute_url(),
        })

    # for p in projects_data:
    #     print(p.get("title"))

    context = {
        'harkat': CrowdFunding.objects.all(),
        'course': Course.objects.all(),
        'forum': Forum.objects.all(),
        'divar': Divar.objects.filter().all(),
        'divars': Divar.objects.filter(Type=0).all(),
        'amanat': Divar.objects.filter(Type=1).all(),
        'jobs': Job.objects.all(),
        'map': projects_data,
        'statistics': {
            'lms': f"{Course.objects.all().count():,}",
            'harkat': f"{CrowdFunding.objects.all().count():,}",
            'madadyar': f"{JahadActivity.objects.all().count():,}",
            'forum': f"{Forum.objects.all().count():,}",
            'job': f"{Job.objects.all().count():,}",
        },
    }
    return render(request, 'home.html', context)
