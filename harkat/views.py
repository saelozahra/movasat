from django.shortcuts import render
from harkat.models import CrowdFunding, Transaction
from django.conf import settings
import json
from django.http import JsonResponse
from django.shortcuts import redirect
import requests

ZP_API_REQUEST = f"https://www.zarinpal.com/pg/rest/WebGate/PaymentRequest.json"
ZP_API_VERIFY = f"https://www.zarinpal.com/pg/rest/WebGate/PaymentVerification.json"
ZP_API_STARTPAY = f"https://www.zarinpal.com/pg/StartPay/"


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
    cf = CrowdFunding.objects.filter(Slug=slug)
    cf.update(view_count=int(cf.get().view_count+1))

    cf = cf.get()
    tr = Transaction.objects.filter(harkat__Slug=slug).all()

    context = {
        "h": cf,
        "t": tr,
        "edit_url": cf.get_edit_url(),
    }

    return render(request, "harkat_single.html", context=context)


def send_pay_request(request):
    Desc = request.POST['description']
    mablagh = request.POST['amount']
    hid = request.POST['hid']
    pname = request.POST['name']
    ptel = request.POST['tel']
    new_tr = Transaction.objects.create(
        harkat_id=hid,
        Purchaser=pname,
        PurchaserTel=ptel,
        PurchaserIP=get_client_ip(request),
        Description=Desc,
        Amount=mablagh,
        Status="N",
    )
    print(f'{settings.HOMEURL}/verify/{new_tr.id}    {mablagh}')
    data = {
        "MerchantID": settings.MERCHANT,
        "Amount": mablagh,
        "Description": f"{Desc}   {new_tr}",
        "Phone": ptel,
        "CallbackURL": f'{settings.HOMEURL}/harkat/pardakht/verify/{new_tr.id}',
    }
    data = json.dumps(data)
    # set content length by data
    headers = {'content-type': 'application/json', 'content-length': str(len(data))}
    try:
        response = requests.post(ZP_API_REQUEST, data=data, headers=headers, timeout=10)

        if response.status_code == 200:
            json_response = response.json()
            if json_response['Status'] == 100:
                redirect_url = ZP_API_STARTPAY + str(json_response['Authority'])
                return redirect(redirect_url)
            else:
                return JsonResponse({'status': False, 'code': str(json_response['Status'])})
        return JsonResponse(response)

    except requests.exceptions.Timeout:
        return {'status': False, 'code': 'timeout'}
    except requests.exceptions.ConnectionError:
        return {'status': False, 'code': 'connection error'}


def verify(authority, tid):

    tr = Transaction.objects.filter(id=tid).get()

    query_params = authority.GET.copy()
    authority_value = query_params.get('Authority', '')


    data = {
        "MerchantID": settings.MERCHANT,
        "Amount": tr.Amount,
        "Authority": authority_value,
    }
    data = json.dumps(data)
    headers = {'content-type': 'application/json', 'content-length': str(len(data))}
    response = requests.post(ZP_API_VERIFY, data=data, headers=headers)

    if response.status_code == 200:
        response_json = response.json()
        if response_json['Status'] == 100:
            Transaction.objects.filter(id=tid).update(
                Status="S",
                PurchaseID=authority_value,
            )
        else:
            Transaction.objects.filter(id=tid).update(
                Status="X",
                PurchaseID=authority_value,
            )
    return redirect(f"{tr.harkat.get_absolute_url()}?payment=success#pay{tr.id}")

