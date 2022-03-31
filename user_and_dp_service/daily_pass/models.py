from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


# Create your models here.

class NoUpdateBaseModel(models.Model):
    class Meta:
        abstract = True

    created_at = models.DateTimeField(default=timezone.now)


class DailyPass(NoUpdateBaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    chapter_id = models.BigIntegerField()
    series_id = models.BigIntegerField()

    class Meta:
        unique_together = ('user', 'chapter_id')

