from django import forms
from django.core.exceptions import ValidationError
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget
from .models import Best20

class BestLecForm(forms.ModelForm):
    class Meta:
        model = Best20
        fields = ['title', 'description', 'url_lec']

        widgets = {
            'description': SummernoteWidget(),
        }

# class CommentForm(forms.ModelForm):
#     class Meta:
#         model = CommentForTodo
#         fields = ('title','file_name','text')
#
#         widgets = {
#             'text': SummernoteWidget(),
#             'bar': SummernoteInplaceWidget(),
#         }
