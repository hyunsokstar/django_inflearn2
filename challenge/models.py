from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django.utils import timezone
from markdownx.models import MarkdownxField
from markdownx.utils import markdown
from django.urls import reverse
from datetime import timedelta

# Create your models here.

# 챌린지 분류
class challenge_subject(models.Model):
	title = models.CharField(max_length=40)
	description = models.CharField(max_length=40)
	leader = models.CharField(max_length=20)
	home = models.CharField(max_length=40)
	created= models.DateTimeField(auto_now_add=True)
	image = models.ImageField(upload_to='wm/%y%m%d', blank=True)

	def lecinfo_count2(self):
		return self.lecinfo_set.count()

	def __str__(self):
		return self.title

# 과목에 대한 챌린지 모임
class LecInfo(models.Model):
	challenge = models.ForeignKey(challenge_subject, on_delete=models.CASCADE)
	lec_name = models.CharField(max_length=40)
	manager = models.CharField(max_length=40)
	lec_url = models.CharField(max_length=120)
	git_url = models.CharField(max_length=120)
	lec_reputation = models.IntegerField(default=0)
	student_count = models.IntegerField(default=0)

	def __str__(self):
		return self.lec_name

	def student_count2(self):
		return self.studentrecord_set.count()

class RecommandLecInfo(models.Model):
    lecinfo = models.ForeignKey(LecInfo, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

class StudentRecord(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    current_class = models.CharField(max_length=40)
    classification = models.ForeignKey(LecInfo, on_delete=models.CASCADE)
    github_url = models.CharField(max_length=120)
    created= models.DateTimeField(auto_now_add=True)
