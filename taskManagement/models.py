from django.db import models

class Task:
    title = models.CharField(max_length=80, blank=False, null=False)
    taskDate = models.DateTimeField(auto_now_add=True, blank=False, null=False)
    location = models.CharField(max_length=80, blank=True, null=True)
    done = models.BooleanField(default=False, blank=False, null=False)
    description = models.CharField(max_length=5000, blank=True, null=True)
