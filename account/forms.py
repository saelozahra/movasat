from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import UserDetail


class RegisterUser(forms.ModelForm):

    class Meta:
        model = UserDetail
        # fields = '__all__'
        fields = ['first_name', 'last_name', 'username', 'tel', 'email', 'melli', 'password', 'City', 'birth', 'skills', ]


class ActiveUser(forms.ModelForm):
    otp = forms.IntegerField(label="کد ورود")

