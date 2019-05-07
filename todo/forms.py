from django import forms
from django.core.exceptions import ValidationError
from .models import Todo

class TodoForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = ['lecture','title', 'content','note' ]
