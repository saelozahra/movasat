from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import UserDetail


class RegisterUser(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(), label="کلمه عبور")

    class Meta:
        model = UserDetail
        # fields = '__all__'
        fields = ['first_name', 'last_name', 'username', 'tel', 'email', 'melli', 'password', 'City', 'birth', 'skills', ]

