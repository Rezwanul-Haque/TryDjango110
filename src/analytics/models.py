from django.db import models
from shortener.models import KirrURL
# Create your models here.

class ClickEventManager(models.Manager):
    """Django data model ClickEventManager"""
    def create_event(self, kirrInstance):
        if isinstance(kirrInstance, KirrURL):
            obj, created = self.get_or_create(kirr_url = kirrInstance)
            obj.count += 1
            obj.save()
            return obj.count
        return None

class ClickEvent(models.Model):
    """Django data model ClickEvent"""
    kirr_url = models.OneToOneField(KirrURL)
    count = models.IntegerField(default = 0)
    updated = models.DateTimeField(auto_now = True)
    timestamp = models.DateTimeField(auto_now_add=True)

    # overwritting default Manager
    objects = ClickEventManager()

    class Meta:
        verbose_name = 'ClickEvent'
        verbose_name_plural = 'ClickEvents'

    def __str__(self):
        return "{i}".format(i = self.count)
