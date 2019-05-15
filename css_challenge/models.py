from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from markdownx.models import MarkdownxField
from markdownx.utils import markdown

# Create your models here.
class CssImage(models.Model):
    title = models.CharField(max_length=50)
    head_image = models.ImageField(upload_to='blog/%y%m%d', blank=True)
    author = models.ForeignKey(User, on_delete=True)
    created = models.DateTimeField(auto_now_add=True)
