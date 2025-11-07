from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
    content = models.CharField(max_length=255)
    time_created = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(to=User, on_delete=models.SET_NULL, null=True)


class Like(models.Model):
    post = models.ForeignKey(to=Post, on_delete=models.CASCADE)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)