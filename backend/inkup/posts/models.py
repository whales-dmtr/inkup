from django.db import models
from django.contrib.auth.models import User


class Posts(models.Model):
    content = models.CharField(max_length=255)
    likes_number = models.IntegerField()
    time_created = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(to=User, on_delete=models.SET_NULL, null=True)

    class Meta:
        constraints = [
            models.CheckConstraint(condition=models.Q(likes_number__gte=0), name='likes_gte_0')
        ]