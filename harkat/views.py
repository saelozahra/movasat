from django.shortcuts import render
from harkat.models import Harkat

# Create your views here.


def percentage(kol, jozea):
    print("______")
    print("kol:", kol, ", joz:", jozea)
    print("j100", int(jozea) * 100)
    print("j", int(jozea) * 100 / int(kol))
    if kol == 0:
        return 0
    elif kol == jozea:
        return 100
    else:
        return int(jozea) * 100 / int(kol)


def harkat_single(request, jahadi, slug):
    harkatdata = Harkat.objects.filter(slug=slug).get()
    data = {
        "data": harkatdata,
        "percent_amount": int(percentage(harkatdata.Amount, harkatdata.TotalAmount))
    }
    return render(request, "harkat_page.html", context={"data": data})
