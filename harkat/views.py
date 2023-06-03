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


def send_pay_request(request):
    Desc = request.POST['description']
    new_tr = Transaction.objects.create(
        harkat_id=request.POST['hid'],
        Purchaser=request.POST['name'],
        PurchaserTel=request.POST['tel'],
        PurchaserIP=get_client_ip(request),
        Description=Desc,
        Amount=request.POST['amount'],
        Status="N",
    )

    data = {
        "MerchantID": settings.MERCHANT,
        "Amount": request.POST['amount'],
        "Description": f"{Desc}   {new_tr}",
        "Phone": request.POST['tel'],
        "CallbackURL": f'{settings.HOMEURL}/verify/{new_tr.id}',
    }
    data = json.dumps(data)
    # set content length by data
    headers = {'content-type': 'application/json', 'content-length': str(len(data))}
    try:
        response = requests.post(ZP_API_REQUEST, data=data, headers=headers, timeout=10)

        print(response.status_code)
        if response.status_code == 200:
            print(2)
            response = response.json()
            if response['Status'] == 100:
                print(3)
                return {'status': True, 'url': ZP_API_STARTPAY + str(response['Authority']),
                        'authority': response['Authority']}
            else:
                print(4)
                return {'status': False, 'code': str(response['Status'])}
        print(5)
        return response

    except requests.exceptions.Timeout:
        return {'status': False, 'code': 'timeout'}
    except requests.exceptions.ConnectionError:
        return {'status': False, 'code': 'connection error'}


def verify(authority, tid):
    tr = Transaction.objects.filter(id=tid).get()
    data = {
        "MerchantID": settings.MERCHANT,
        "Amount": tr.Amount,
        "Authority": authority,
    }
    data = json.dumps(data)
    # set content length by data
    headers = {'content-type': 'application/json', 'content-length': str(len(data))}
    response = requests.post(ZP_API_VERIFY, data=data, headers=headers)

    if response.status_code == 200:
        response = response.json()
        if response['Status'] == 100:
            return {'status': True, 'RefID': response['RefID']}
        else:
            return {'status': False, 'code': str(response['Status'])}
    return response
