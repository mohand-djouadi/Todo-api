from django.db import models
from django.conf import settings

class Task(models.Model):

    NOT_STARTED = 'NOT_STARTED'
    IN_PROGRESS = 'IN_PROGRESS'
    PENDING = 'PENDING'
    COMPLETED = 'COMPLETED'
    ON_HOLD = 'ON_HOLD'
    CANCELED = 'CANCELED'

    CHOICES_STATUS = (
        (NOT_STARTED, 'Not started'),
        (IN_PROGRESS, 'In progress'),
        (PENDING, 'Pending'),
        (COMPLETED, 'Completed'),
        (ON_HOLD, 'On hold'),
        (CANCELED, 'Canceled')
    )

    title = models.CharField(max_length=80, blank=False, null=False)
    location = models.CharField(max_length=80, blank=True, null=True)
    taskDate = models.DateTimeField(blank=False, null=False)
    status = models.CharField(max_length=80, choices=CHOICES_STATUS, default=NOT_STARTED, null=False)
    description = models.CharField(max_length=5000, blank=True, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE)

    @classmethod
    def get_status_value(cls, label):
        status_dict = dict(cls.CHOICES_STATUS)
        for key, value in status_dict.items():
            if value == label:
                return key

    def update_fields(self, **kwargs):
        for field, value in kwargs.items():
            if field in ['title', 'location', 'taskDate', 'status', 'description']:
                setattr(self, field, value)
        if 'status' in kwargs:
            self.status = self.get_status_value(self.status)
        self.save()

class Comment(models.Model):
    content = models.CharField(max_length=1200, blank=False, null=False)
    createdAt = models.DateTimeField(blank=False, null=False)
    task = models.ForeignKey(Task, null=True, on_delete=models.CASCADE)