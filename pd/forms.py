from django import forms
from django.core.exceptions import ValidationError
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget
from .models import MyTask

class MyTaskForm(forms.ModelForm):
    class Meta:
        model = MyTask
        fields = ['title', 'github', 'content','shortcut_id']
