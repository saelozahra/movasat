from django.urls import reverse
from django.views.generic import TemplateView
from harkat.models import Project
from django.shortcuts import render
from django.http import Http404, HttpResponseRedirect
from .models import Forum, Response, Divar


# Create your views here.


class ForumView(TemplateView):
    def post(self, request, **kwargs):
        uid = request.POST["uid"]
        fid = request.POST["fid"]
        description = request.POST["description"]
        file = request.POST["file"]
        Response.objects.create(
            RelatedForum_id=fid,
            description=description,
            file=file,
            writer_id=uid,
        )
        return HttpResponseRedirect(reverse("show_forum", kwargs={"fid": fid, }))

    def get(self, request, **kwargs):
        fid = kwargs.get("fid")
        try:
            context = {
                "project": Project.objects.filter(id=fid).get(),
                "forum": Forum.objects.filter(id=fid).get(),
                "response": Response.objects.filter(RelatedForum_id=fid).all(),
                "edit_url": Forum.objects.filter(id=fid).get().get_edit_url(),
            }
        except Forum.DoesNotExist:
            raise Http404
        return render(request, "forum.html", context=context)


def show_challenge_cat(request, c_cat_slug):
    try:
        context = {
            "forum": Forum.objects.filter(RelatedProject__ProjectCat=c_cat_slug).all(),
        }
    except Forum.DoesNotExist:
        raise Http404
    return render(request, "challenge_page.html", context=context)


def all_challenges(request):
    try:
        context = {
            "forum": Forum.objects.all(),
        }
    except Forum.DoesNotExist:
        raise Http404
    return render(request, "challenge_page.html", context=context)


class DivarView(TemplateView):
    def get(self, request, **kwargs):
        did = kwargs.get("did")
        try:
            context = {
                "divar": Divar.objects.filter(id=did).get(),
                "edit_url": Divar.objects.filter(id=did).get().get_edit_url(),
            }
        except Forum.DoesNotExist:
            raise Http404
        return render(request, "DivarSingle.html", context=context)
