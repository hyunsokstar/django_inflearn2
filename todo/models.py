from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django.utils import timezone

class Todo(models.Model):
    lecture = models.CharField(max_length=100, blank=True)
    title = models.CharField(max_length=30)
    content = models.TextField()
    created = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=True)
    note = models.CharField(max_length=50)
    elapsed_time = models.CharField(max_length=20)

    @property
    def now_diff(self):
        return timezone.now() - self.created

class TodoComplete(models.Model):
    lecture = models.CharField(max_length=100, blank=True)
    title = models.CharField(max_length=30)
    content = models.TextField()
    created = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=True)
    note = models.TextField(blank=True)
    elapsed_time = models.DateTimeField(null=True, default = None)
