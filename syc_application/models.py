from django.db import models
from django.conf import settings


# Create your models here.

class Script(models.Model):
    name = models.CharField(max_length=50, unique=True)
    context = models.CharField(max_length=200, null=False, blank=False)


class ExcuteInfo(models.Model):
    celery_id = models.CharField(max_length=255,primary_key=True)
    context = models.CharField(max_length=255, unique=True, null=False, blank=False)
    excute_time = models.DateTimeField(auto_now_add=True)

