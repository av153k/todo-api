from django.db import models
import datetime
from authentication.models import User
from django.conf import settings
# Create your models here.


class Tasks(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    task_name = models.CharField(max_length=200)
    completed = models.BooleanField(default=False, blank=True, null=True)
    created_at = models.DateTimeField(default=datetime.datetime.now)
    objects = models.Manager()

    def __str__(self):
        return self.task_name
