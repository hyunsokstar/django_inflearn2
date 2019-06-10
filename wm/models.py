from django.db import models
from markdownx.models import MarkdownxField
from markdownx.utils import markdown
from django.contrib.auth.models import User

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=25, unique=True)
    description = models.TextField(blank=True)
    slug = models.SlugField(unique=True, allow_unicode=True)
    author = models.ForeignKey(User, on_delete=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
            return '/wm/myshortcut/category/{}/'.format(self.slug)

class Type(models.Model):
    type_name = models.CharField(max_length=20)

    def __str__(self):
        return self.type_name

class MyShortCut(models.Model):
    title = models.CharField(max_length=120)
    content1 = models.CharField(max_length=180)
    content2 = models.TextField(blank=True)
    created = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=True)
    category = models.ForeignKey(Category, blank=True, null=True, on_delete=models.SET_NULL)
    type= models.ForeignKey(Type, on_delete=models.CASCADE)
