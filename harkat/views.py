from django.shortcuts import render
from harkat.models import Harkat

# Create your views here.

def harkat_single(request, jahadi, slug):
    harkatdata = Harkat.objects.filter(slug=slug).get()
    data = {
        "data": harkatdata,
        "percent_amount": int(percentage(harkatdata.Amount, harkatdata.TotalAmount))
    }
    return render(request, "harkat_page.html", context={"data": data})
