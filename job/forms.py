import home.models
from django import forms
from location_field.forms.plain import PlainLocationField

from .models import Job


class RegisterJob(forms.ModelForm):
    def __init__(self, *args, **kwargs):

        try:
            self.register_job = home.models.Box.objects.filter(location="register_job").get()
        except home.models.Box.DoesNotExist:
            self.register_job = ""

        super().__init__(*args, **kwargs)

    class Meta:
        model = Job
        fields = '__all__'
        exclude = ['owner']
