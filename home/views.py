from harkat.models import Harkat
from lms.models import Course
from madadyar.models import JahadActivity
from django.shortcuts import render

# Create your views here.


def home_view(request):

    context = {
        'course': Course.objects.all(),
        'statistics': {
            'lms': f"{Course.objects.all().count():,}",
            'harkat': f"{Harkat.objects.all().count():,}",
            'madadyar': f"{JahadActivity.objects.all().count():,}",
        },
    }
    return render(request, 'home.html', context)
