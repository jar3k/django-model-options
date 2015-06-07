from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models


class OptionBase(models.Model):

    key = models.CharField(max_length=255)
    value = models.CharField(max_length=255)

    class Meta:
        abstract = True

    def __str__(self):
        return self.value


class Option(OptionBase):

    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        unique_together = ('content_type', 'object_id', 'key')
