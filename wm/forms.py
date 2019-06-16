from django import forms
from django.core.exceptions import ValidationError
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget
from .models import MyShortCut

# category 모델이 foreignkey인데
# 입력시 카테고리 선택 목록의 내용들에 (author = 본인)의 조건을 걸고 싶다.
class MyShortCutForm_input(forms.ModelForm):
    class Meta:
        model = MyShortCut
        fields = ['title', 'content1']

class MyShortCutForm_input_title(forms.ModelForm):
    class Meta:
        model = MyShortCut
        fields = ['title','content2']

class MyShortCutForm_summer_note(forms.ModelForm):
    class Meta:
        model = MyShortCut
        fields = ['title', 'content2']

        widgets = {
            'content2': SummernoteWidget(),
        }
