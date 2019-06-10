from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=100)
    completecount = models.IntegerField(default=0)
    uncompletecount = models.IntegerField(default=0)
    reputation = models.IntegerField(default=0)
    shortcut_user_id = models.CharField(default="me", max_length=40)
    selected_category_id = models.IntegerField(default=1, blank=True)
