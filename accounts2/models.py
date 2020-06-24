from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from todo.models import TeamInfo

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=100)
    completecount = models.IntegerField(default=0)
    uncompletecount = models.IntegerField(default=0)
    reputation = models.IntegerField(default=0)
    shortcut_user_id = models.CharField(default="me", max_length=40)
    selected_category_id = models.IntegerField(default=1, blank=True)
    team = models.ForeignKey(TeamInfo, on_delete=models.CASCADE, null=True, blank=True)
    position = models.CharField(max_length=50,default="member")
    subject_of_memo = models.CharField(max_length=60) # 스킬 노트의 주제
    skill_note_reputation = models.IntegerField(default=0) # skill note 유저 리스트 점수 추가할때 계산됨
    email = models.CharField(max_length=20 , blank=True)
    public = models.CharField(max_length=5 , default="yes")
    github= models.CharField(max_length=20 , default="www.github.com")
    site2 = models.CharField(max_length=20 , blank=True)
    site1 = models.CharField(max_length=20 , blank=True)
    site3 = models.CharField(max_length=20 , blank=True)
    site4 = models.CharField(max_length=20 , blank=True)
