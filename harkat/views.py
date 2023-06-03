from django.shortcuts import render
from harkat.models import CrowdFunding, Transaction

# Create your views here.


def harkat_page(request):

    data = CrowdFunding.objects.filter().all()
    return render(request, "harkat_page.html", context={"harkat": data})


def harkat_single(request, jahadi, slug):
    cf = CrowdFunding.objects.filter(Slug=slug).get()
    tr = Transaction.objects.filter(harkat__Slug=slug).all()
    return render(request, "harkat_single.html", context={"h": cf, "t": tr, })
