from django.shortcuts import render
from .models import Forum
# Create your views here.


def show_forum(request, fid):
    fdata = Forum.objects.filter(id=fid).get()
    context = {
        "forum": fdata,
    }
    return render(request, "forum.html", context=context)
