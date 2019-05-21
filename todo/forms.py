from django import forms
from django.core.exceptions import ValidationError
from .models import Todo, CommentForTodo

class TodoForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = ['title', 'content']

class CommentForm(forms.ModelForm):
    class Meta:
        model = CommentForTodo
        fields = ('title','file_name','text')
