from django.db import models
from django.utils import timezone


class BaseModel(models.Model):
    class Meta:
        abstract = True

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)


class Series(BaseModel):
    title = models.CharField(max_length=255, unique=True)


class Chapter(BaseModel):
    class Meta:
        unique_together = ('title', 'series')

    title = models.CharField(max_length=255)
    series = models.ForeignKey(Series, related_name='chapters', on_delete=models.CASCADE)
