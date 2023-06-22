import random
import requests
from django.contrib.auth.hashers import make_password
from django.http import HttpResponse
from .forms import RegisterUser
from django.shortcuts import render, redirect
from django.views.generic import TemplateView, CreateView

from account.models import *
from harkat.models import CrowdFunding, Project
from madadyar.models import MadadJoo


# Create your views here.

class MadadJooHa(TemplateView):
    pass
    # def get(self, request, **kwargs):
    #     # chat_id = kwargs.get("chat_id")
    #     all_course = account.models.MadadJoo.objects.order_by("CreatedDate")
    #
    #     if not self.request.user.is_authenticated:
    #         return HttpResponseRedirect('../../')
    #
    #     context = {
    #         'Cource': all_course,
    #     }
    #
    #     return render(request, 'course.html', context)


def list_madadjooha(request, slug):
    context = {
        # 'ForMobile': for_mobile,
        'madadjooha': MadadJoo.objects.all(),
    }
    return render(request, 'lesson.html', context)


def get_profile(request, user):
    data = []
    model = ""
    if MadadJoo.objects.filter(user__username=user).exists():
        model = "j"
        data = MadadJoo.objects.filter(user__username=user).get()
    elif MadadKar.objects.filter(user__username=user).exists():
        model = "k"
        data = MadadKar.objects.filter(user__username=user).get()
    harkat = CrowdFunding.objects.filter(MadadKar__user__username=user).all()
    project = Project.objects.filter(madadkar__user__username=user).order_by("-date").all()

    context = {
        'harkat': harkat,
        'project': project,
        'data': data,
        'model': model
    }
    return render(request, 'profile.html', context=context)


class UserCreate(CreateView):
    form_class = RegisterUser
    template_name = "reg_user.html"

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.otp = random.randint(1000, 9999)
        user.password = make_password(form.cleaned_data['password'])
        user.save()
        tel = form.cleaned_data.get("tel")

        # send msg
        url = "http://rest.payamak-panel.com/api/SendSMS/BaseServiceNumber"
        payload = f"username=sael&password=6cbc37ef-6273-43ad-85c0-0c8d5feff897&to={tel}&bodyId=146403&" \
                  f"text={user.get_full_name()};{user.otp}"
        headers = {"Content-Type": "application/x-www-form-urlencoded"}

        response = requests.request("POST", url, data=payload.encode(), headers=headers)

        print(HttpResponse(response))
        print(response.text)

        return redirect("user_active", uid=user.id)


def user_active(request, uid):
    msg = "کد پیامک شده را در اینجا وارد کنید"
    if request.POST:
        otp = request.POST['otp']
        user = UserDetail.objects.get(id=uid)
        if int(user.otp) == int(otp):
            user.is_active = True
            user.save()
            return redirect("index")
        else:
            msg = "کد وارد شده صحیح نیست"
    context = {
        "msg": msg,
        "user": {"id": uid},
    }
    return render(request, "activation.html", context=context)
