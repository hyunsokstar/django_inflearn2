from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=30)
    content = models.TextField()
    head_image = models.ImageField(upload_to='blog/%y%m%d', blank=True)
    created = models.DateTimeField()
    author = models.ForeignKey(User, on_delete=True)

    def __str__(self):
        return '{}::{}'.format(self.title, self.author)

    def get_absolute_url(self):
        return reverse('blog:post_detail', args=[self.id])
