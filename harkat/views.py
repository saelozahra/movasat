from django.shortcuts import render
from harkat.models import CrowdFunding

# Create your views here.


def harkat_page(request):

    data = CrowdFunding.objects.filter().all()
    return render(request, "harkat_page.html", context={"harkat": data})


def harkat_single(request, jahadi, slug):
    data = CrowdFunding.objects.filter(slug=slug).get()
    return render(request, "harkat_item.html", context={"harkat": data})
