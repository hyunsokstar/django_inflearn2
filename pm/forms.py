from django import forms
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget
from .models import Manual

class ManualForm(forms.ModelForm):
    class Meta:
        model = Manual
        fields = ['title', 'url' ,'photo', 'content']

        widgets = {
            'content': SummernoteWidget(),
        }
