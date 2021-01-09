from django import forms
from django.forms import ModelForm
from . import models

class PatientProfile(ModelForm):
    class Meta:
        model = models.App_User
        fields = ['first_name', 'last_name', 'address', 'city', 'pincode', 'country', 'aboutme','user']


class ReportUploadForm(ModelForm):

    class Meta:
        model = models.Report
        fields = ('__all__')

    def __init__(self, *args, **kwargs):
        super(ReportUploadForm, self).__init__(*args, **kwargs)
        self.fields['doctor'].widget = forms.HiddenInput()

    