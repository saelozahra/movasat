from harkat.models import Project
from django.shortcuts import render
from django.http import Http404
from .models import Forum, Response
# Create your views here.


def show_forum(request, fid):
    try:
        context = {
            "project": Project.objects.filter(id=fid).get(),
            "forum": Forum.objects.filter(id=fid).get(),
            "response": Response.objects.filter(RelatedForum_id=fid).all(),
        }
    except Forum.DoesNotExist:
        raise Http404
    return render(request, "forum.html", context=context)
