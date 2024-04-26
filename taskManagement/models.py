from django.db import models
from django.conf import settings

class Task(models.Model):
    title = models.CharField(max_length=80, blank=False, null=False)
    location = models.CharField(max_length=80, blank=True, null=True)
    taskDate = models.DateTimeField(blank=False, null=False)
    done = models.BooleanField(default=False, blank=False, null=False)
    description = models.CharField(max_length=5000, blank=True, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE)