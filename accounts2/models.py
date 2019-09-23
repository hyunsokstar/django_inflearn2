from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from todo.models import TeamInfo

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=100)
    completecount = models.IntegerField(default=0)
    uncompletecount = models.IntegerField(default=0)
    reputation = models.IntegerField(default=0)
    shortcut_user_id = models.CharField(default="me", max_length=40)
    selected_category_id = models.IntegerField(default=1, blank=True)
    team = models.ForeignKey(TeamInfo, on_delete=True, null=True, blank=True)
    position = models.CharField(max_length=50,default="member")
    subject_of_memo = models.CharField(max_length=60)
