import random
import account
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
import json

from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
# Create your views here.


@method_decorator(csrf_exempt, name='dispatch')
class OTPStart(TemplateView):
    def post(self, request, **kwargs):
        username = kwargs.get("username")
        print("kwarg: ", username)
        print("username: ", username)
        print("first: ", User.objects.first())
        if username is None:
            return HttpResponse(json.dumps({'status': "error", 'description': "please enter user", }),
                                content_type='application/json')
        otp_user = User.objects.get(username=username)
        print("otp user: ", otp_user)
        new_token = random.randint(1000, 9999)
        phone = otp_user.userdetail.phone
        name = otp_user.get_full_name()
        if phone.__len__() > 9:
            import requests
            url = "http://rest.payamak-panel.com/api/SendSMS/BaseServiceNumber"
            payload = f"username=sael&password=6cbc37ef-6273-43ad-85c0-0c8d5feff897&to={phone}&bodyId=108091&text={name};{new_token}"
            headers = {"Content-Type": "application/x-www-form-urlencoded"}

            response = requests.request("POST", url, data=payload.encode(), headers=headers)

            print(HttpResponse(response))
            print(response.text)

            otp_data_to_dump = {
                'status': "success",
                'name': name,
                'tel': phone,
                'response': response.text,
            }
        else:
            otp_data_to_dump = {
                'status': "error",
                'description': "user not found",
            }
        data = json.dumps(otp_data_to_dump)
        return HttpResponse(data, content_type='application/json')


class OTPValidate(TemplateView):
    def post(self, request, **kwargs):
        username = kwargs.get("username")
        otp_code = kwargs.get("code")
        otp_user = User.objects.filter(username=username).get()
        phone = otp_user.userdetail.phone
        name = otp_user.get_full_name()
        if otp_user.userdetail.otp == otp_code:
            otp_data_to_dump = {
                'status': "success",
                'name': name,
                'tel': phone,
            }
        else:
            otp_data_to_dump = {
                'status': "error",
                'description': "otp not equal",
            }
        data = json.dumps(otp_data_to_dump)
        return HttpResponse(data, content_type='application/json')


class MadadJooHa(TemplateView):
    def get(self, request, **kwargs):
        # chat_id = kwargs.get("chat_id")
        all_course = account.models.MadadJoo.objects.order_by("CreatedDate")

        if not self.request.user.is_authenticated:
            return HttpResponseRedirect('../../')

        context = {
            'Cource': all_course,
        }

        return render(request, 'course.html', context)


def list_madadjooha(request, slug):

    context = {
        # 'ForMobile': for_mobile,
        'madadjooha': account.models.MadadJoo.objects.all(),
    }
    return render(request, 'lesson.html', context)