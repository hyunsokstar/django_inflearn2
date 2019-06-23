from django import forms
from django.core.exceptions import ValidationError
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget
from .models import LecInfo

# from bootstrap_datepicker_plus import DatePickerInput

class LecInfoForm(forms.ModelForm):
    class Meta:
        model = LecInfo
        fields = ['lec_name','teacher', 'lec_url','git_url']
