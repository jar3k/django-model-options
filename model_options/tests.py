import mock

from django.db import models
from django.test import TestCase

from .mixins import CachedOptionsMixin, OptionsMixin
from .models import Option
from .utils import detect_type, sync_models


class OptionMixinTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        class OptionsModel(OptionsMixin, models.Model):
            pass
        sync_models([OptionsModel])
        cls.model_obj = OptionsModel

    def setUp(self):
        self.model = self.model_obj.objects.create()

    def test_add_option(self):
        self.model.set_option('foo', 'bar')
        option = Option.objects.get().value
        self.assertEqual(option, 'bar')

    def test_override_option(self):
        self.model.set_option('foo', 'bar')
        self.model.set_option('foo', 'example')
        option = Option.objects.get().value
        self.assertEqual(option, 'example')

    def test_delete_option(self):
        self.model.set_option('foo', 'bar')
        self.assertEqual(Option.objects.count(), 1)
        self.model.delete_option('foo')
        self.assertEqual(Option.objects.count(), 0)

    def test_delete_not_existing_option(self):
        self.assertRaises(Option.DoesNotExist,
                          lambda: self.model.delete_option('foo'))

    def test_has_option(self):
        self.model.set_option('foo', 'bar')
        self.assertTrue(self.model.has_option('foo'))

    def test_has_not_option(self):
        self.assertFalse(self.model.has_option('foo'))

    def test_get_option(self):
        self.model.set_option('foo', 'bar')
        self.model.set_option('fiz', 'baz')
        model_option = self.model.get_option('foo')
        option = Option.objects.get(key='foo').value
        self.assertEqual(option, model_option)

    def test_get_default_option(self):
        model_option = self.model.get_option('foo')
        self.assertEqual(model_option, None)

    def test_get_custom_default_option(self):
        model_option = self.model.get_option('foo', 'fizbaz')
        self.assertEqual(model_option, 'fizbaz')


class CachedOptionMixinTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        class CachedOptionsModel(CachedOptionsMixin, models.Model):
            pass
        sync_models([CachedOptionsModel])
        cls.model_obj = CachedOptionsModel

    def setUp(self):
        self.model = self.model_obj.objects.create()

    @mock.patch('model_options.mixins.cache')
    def test_add_option(self, cache):
        self.model.set_option('foo', 'bar')
        cache.set.assert_called_once_with(
            'model_options-cachedoptionsmodel-foo',
            'bar'
        )

    @mock.patch('model_options.mixins.cache')
    def test_delete_option(self, cache):
        self.model.delete_option('foo')
        cache.delete.assert_called_once_with(
            'model_options-cachedoptionsmodel-foo'
        )

    @mock.patch('model_options.mixins.cache')
    def test_has_option(self, cache):
        self.model.has_option('foo')
        cache.get.assert_called_once_with(
            'model_options-cachedoptionsmodel-foo'
        )

    @mock.patch('model_options.mixins.cache')
    def test_get_option(self, cache):
        cache.get = mock.Mock(return_value='bar')
        option = self.model.get_option('foo')
        self.assertEqual(option, 'bar')

    @mock.patch('model_options.mixins.cache')
    def test_get_default_option(self, cache):
        cache.get = mock.Mock(return_value=None)
        model_option = self.model.get_option('foo')
        self.assertEqual(model_option, None)

    @mock.patch('model_options.mixins.cache')
    def test_get_custom_default_option(self, cache):
        cache.get = mock.Mock(return_value=None)
        model_option = self.model.get_option('foo', 'bar')
        self.assertEqual(model_option, 'bar')


class DetectTypeTest(TestCase):

    def test_bool_false(self):
        detected = detect_type(False)
        self.assertEqual(detected, False)
        self.assertIsInstance(detected, bool)

    def test_bool_true(self):
        detected = detect_type(True)
        self.assertEqual(detected, True)
        self.assertIsInstance(detected, bool)

    def test_bool_string_False(self):
        detected = detect_type('False')
        self.assertEqual(detected, False)
        self.assertIsInstance(detected, bool)

    def test_bool_string_false(self):
        detected = detect_type('false')
        self.assertEqual(detected, False)
        self.assertIsInstance(detected, bool)

    def test_bool_string_True(self):
        detected = detect_type('True')
        self.assertEqual(detected, True)
        self.assertIsInstance(detected, bool)

    def test_bool_string_true(self):
        detected = detect_type('true')
        self.assertEqual(detected, True)
        self.assertIsInstance(detected, bool)

    def test_float(self):
        detected = detect_type(1.23)
        self.assertEqual(detected, 1.23)
        self.assertIsInstance(detected, float)

    def test_float_string(self):
        detected = detect_type('1.23')
        self.assertEqual(detected, 1.23)
        self.assertIsInstance(detected, float)

    def test_int(self):
        detected = detect_type(123)
        self.assertEqual(detected, 123)
        self.assertIsInstance(detected, int)

    def test_int_string(self):
        detected = detect_type('123')
        self.assertEqual(detected, 123)
        self.assertIsInstance(detected, int)

    def test_none(self):
        detected = detect_type(None)
        self.assertTrue(detected is None)

    def test_none_string(self):
        detected = detect_type('None')
        self.assertTrue(detected is None)

    def test_string(self):
        detected = detect_type('foo')
        self.assertEqual(detected, 'foo')
        self.assertIsInstance(detected, str)
