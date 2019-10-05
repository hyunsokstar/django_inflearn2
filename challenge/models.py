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

    def __str__(self):
        return self.lec_name

class RecommandLecInfo(models.Model):
    lecinfo = models.ForeignKey(LecInfo, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

class StudentRecord(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    current_class = models.CharField(max_length=40)
    classification = models.ForeignKey(LecInfo, on_delete=models.CASCADE)
    github_url = models.CharField(max_length=120)
    created= models.DateTimeField(auto_now_add=True)
