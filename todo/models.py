from django.contrib.auth.models import User
from django.db import models


class Task(models.Model):
    title = models.CharField(max_length=50, blank=True)
    text = models.CharField(max_length=140, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    complete = models.BooleanField(default=False)
    created_at = models.DateField(auto_now_add=True)
    is_important = models.BooleanField(default=False)
    


