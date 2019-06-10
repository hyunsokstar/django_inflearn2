from django import forms
from django.core.exceptions import ValidationError
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget

# class BestLecForm(forms.ModelForm):
#     class Meta:
#         model = Best20
#         fields = ['title', 'description', 'url_lec']
#
#         widgets = {
#             'description': SummernoteWidget(),
#         }
