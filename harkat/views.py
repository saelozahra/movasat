from django.shortcuts import render
from harkat.models import CrowdFunding, Transaction
from django.conf import settings
import json
import requests

# ? sandbox merchant
if settings.SANDBOX:
    sandbox = 'sandbox'
else:
    sandbox = 'www'

ZP_API_REQUEST = f"https://{sandbox}.zarinpal.com/pg/rest/WebGate/PaymentRequest.json"
ZP_API_VERIFY = f"https://{sandbox}.zarinpal.com/pg/rest/WebGate/PaymentVerification.json"
ZP_API_STARTPAY = f"https://{sandbox}.zarinpal.com/pg/StartPay/"


# Create your views here.
def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def harkat_page(request):

    data = CrowdFunding.objects.filter().all()
    return render(request, "harkat_page.html", context={"harkat": data})


def harkat_single(request, jahadi, slug):
    cf = CrowdFunding.objects.filter(Slug=slug).get()
    tr = Transaction.objects.filter(harkat__Slug=slug).all()
    return render(request, "harkat_single.html", context={"h": cf, "t": tr, })
