from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django.utils import timezone
from markdownx.models import MarkdownxField
from markdownx.utils import markdown
from django.urls import reverse
from datetime import timedelta

# Create your models here.
class LecInfo(models.Model):
    lec_name = models.CharField(max_length=40)
    teacher = models.CharField(max_length=40)
    lec_url = models.CharField(max_length=120)
    git_url = models.CharField(max_length=120)
    rec_reputation = models.IntegerField(default=0)
    student_count = models.IntegerField(default=0)

class StudentRecord(models.Model):
    author = models.ForeignKey(User, on_delete=True)
    current_class = models.CharField(max_length=40)
    classification = models.ForeignKey(LecInfo, on_delete=True)
    note = models.CharField(max_length=120)
    youtube = models.CharField(max_length=120)
    git_url = models.CharField(max_length=120)
    created= models.DateTimeField(auto_now_add=True)
