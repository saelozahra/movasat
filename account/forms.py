from django import forms
from django.contrib.auth.models import User
from .models import UserDetail


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class RegisterUser(forms.ModelForm):
    def __int__(self, *args, **kwargs):
        super(RegisterUser, self).__init__(*args, **kwargs)

        self.fields["tel"].disabled = True
        self.fields["melli"].disabled = True

        class Meta:
            model = UserDetail
            fields = ['tel', 'City', 'birth', 'skills', 'melli']
