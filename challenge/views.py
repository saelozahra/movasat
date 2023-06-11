from django.shortcuts import render
from django.http import Http404
from .models import Forum, Response
# Create your views here.


def show_forum(request, fid):
    try:
        fdata = Forum.objects.filter(id=fid).get()
        rdata = Response.objects.filter(RelatedForum_id=fid).all()
        context = {
            "forum": fdata,
            "response": rdata,
        }
    except Forum.DoesNotExist:
        raise Http404
    return render(request, "forum.html", context=context)
