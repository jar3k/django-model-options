from django.contrib.contenttypes.fields import GenericRelation
from django.core.cache import cache
from django.db import models, IntegrityError, transaction

from .utils import detect_type
from .models import Option


class OptionsMixin(models.Model):

    options = GenericRelation(Option)

    class Meta:
        abstract = True

    def delete_option(self, key):
        self.options.get(key=key).delete()

    def get_option(self, key, default=None):
        try:
            option = self.options.get(key=key)
            return detect_type(option.value)
        except Option.DoesNotExist:
            return default

    def has_option(self, key):
        return bool(self.options.filter(key=key).exists())

    def set_option(self, key, value=True):
        try:
            with transaction.atomic():
                self.options.create(key=key, value=value)
        except IntegrityError:
            option = self.options.get(key=key)
            option.value = value
            option.save()


class CachedOptionsMixin(object):

    @property
    def cache_key_prefix(self):
        return "{}-{}".format(self._meta.app_label, self._meta.model_name)

    def delete_option(self, key):
        cache.delete(self._get_cache_key(key))

    def get_option(self, key, default=None):
        option = self._get_option(key)
        return detect_type(option) if option else default

    def has_option(self, key):
        return bool(self._get_option(key))

    def set_option(self, key, value=True):
        cache.set(self._get_cache_key(key), value)

    def _get_cache_key(self, key):
        return "{}-{}".format(self.cache_key_prefix, key)

    def _get_option(self, key):
        return cache.get(self._get_cache_key(key))
