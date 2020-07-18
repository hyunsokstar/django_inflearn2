from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class MyTask(models.Model):
    title = models.CharField(max_length=50)
    github = models.CharField(max_length= 100)
    shortcut_id = models.CharField(max_length= 60)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    content = models.TextField(blank=True)
    plan1 = models.TextField(blank=True)
    complete_task1 = models.TextField(blank=True)
    plan2 = models.TextField(blank=True)
    complete_task2 = models.TextField(blank=True)

    def __str__(self):
        return self.title

# Create your models here.
class MySite(models.Model):
    site_name = models.CharField(max_length=50)
    site_url = models.CharField(max_length= 100)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.site_name
