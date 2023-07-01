from django import forms
from location_field.forms.plain import PlainLocationField

from .models import Job


class RegisterJob(forms.ModelForm):

    class Meta:
        model = Job
        fields = '__all__'
        exclude = ['owner']
