from django.db import models
from markdownx.models import MarkdownxField
from markdownx.utils import markdown
from django.contrib.auth.models import User

# Create your models here.
class Type(models.Model):
    type_name = models.CharField(max_length=20)

    def __str__(self):
        return self.type_name

class MyShortCut(models.Model):
    title = models.CharField(max_length=50)
    content1 = models.CharField(max_length=50)
    content2 = models.TextField(blank=True)
    created = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=True)
    type= models.ForeignKey(Type, on_delete=models.CASCADE)
