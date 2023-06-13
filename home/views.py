from challenge.models import Forum
from harkat.models import CrowdFunding
from lms.models import Course
from madadyar.models import JahadActivity
from django.shortcuts import render

# Create your views here.


def home_view(request):

    context = {
        'harkat': CrowdFunding.objects.all(),
        'course': Course.objects.all(),
        'forum': Forum.objects.all(),
        'statistics': {
            'lms': f"{Course.objects.all().count():,}",
            'harkat': f"{CrowdFunding.objects.all().count():,}",
            'madadyar': f"{JahadActivity.objects.all().count():,}",
            'forum': f"{Forum.objects.all().count():,}",
        },
    }
    return render(request, 'home.html', context)
