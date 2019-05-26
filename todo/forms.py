from django import forms
from django.core.exceptions import ValidationError
from .models import Todo, CommentForTodo

from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget

class TodoForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = ['title', 'content']

        widgets = {
            'content': SummernoteWidget(),
        }

class TodoAdminForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = ['author','title', 'content']

        widgets = {
            'content': SummernoteWidget(),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = CommentForTodo
        fields = ('title','file_name','text')

        widgets = {
            'text': SummernoteWidget(),
            'bar': SummernoteInplaceWidget(),
        }
