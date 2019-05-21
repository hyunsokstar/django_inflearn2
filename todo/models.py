from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django.utils import timezone
from markdownx.models import MarkdownxField
from markdownx.utils import markdown
from django.urls import reverse

from datetime import timedelta

class Category(models.Model):
    name = models.CharField(max_length=25, unique=True)
    description = models.TextField(blank=True)
    slug = models.SlugField(unique=True, allow_unicode=True)

    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural = 'categories'
    def get_absolute_url(self):
        return '/todo/category/{}/'.format(self.slug)

class Todo(models.Model):
    lecture = models.CharField(max_length=100, blank=True)
    title = models.CharField(max_length=50)
    content = MarkdownxField()
    created = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=True)
    note = models.CharField(max_length=50)
    elapsed_time = models.CharField(max_length=20,blank=True, null=True)
    category = models.ForeignKey(Category, blank=True, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.title

    def get_markdown_content(self):
        return markdown(self.content)

    def now_diff(self):
        delta = timezone.now() - self.created
        return str(delta - timedelta(microseconds=delta.microseconds))

    def get_absolute_url(self):
        return reverse('todo:todo_detail', args=[self.id])


class CommentForTodo(models.Model):
    todo= models.ForeignKey(Todo, on_delete=models.CASCADE)
    title= models.CharField(max_length=50)
    file_name = models.CharField(max_length= 30)
    text = MarkdownxField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def get_markdown_content(self):
        return markdown(self.text)

    def get_absolute_url(self):
        return reverse('todo:todo_list')
