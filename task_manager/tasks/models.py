from django.db import models
from django.contrib.auth.models import User


class Task(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    status = models.ForeignKey('statuses.Status', on_delete=models.PROTECT,
                               related_name='tasks')
    creator = models.ForeignKey(User, on_delete=models.PROTECT,
                                related_name='created_tasks')
    executor = models.ForeignKey(User, on_delete=models.PROTECT,
                                 related_name='assigned_tasks', null=True,
                                 blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.name
