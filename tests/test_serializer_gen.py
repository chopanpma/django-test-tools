from django.conf import settings
from django.test import TestCase

from django_test_tools.app_manager import DjangoAppManager
from django_test_tools.file_utils import temporary_file
from django_test_tools.generators.serializer_gen import SerializerGenerator, AppSerializerGenerator
from tests.test_model_test_gen import PythonWritingTestMixin


class TestSerializerGenerator(PythonWritingTestMixin, TestCase):
    @temporary_file('py', delete_on_exit=True)
    def test_app_str(self):
        app_name = settings.TEST_APP
        app_manager = DjangoAppManager()
        model = app_manager.get_model(app_name, 'Server')
        model_serializer = SerializerGenerator(model)
        hash = self.write_generator_to_file(self.test_app_str.filename, model_serializer)
        if app_name == 'example.servers':
            self.assertEqual('574fb193778e3bfcec65fe0fa4a0e56eace86280', hash)
        else:
            self.assertEqual(hash, '574fb193778e3bfcec65fe0fa4a0e56eace86280')


class TestAppSerializerGenerator(PythonWritingTestMixin, TestCase):
    @temporary_file('py', delete_on_exit=True)
    def test_app_str(self):
        app_name = settings.TEST_APP
        app_manager = DjangoAppManager()
        app = app_manager.get_app(app_name)
        app_serializers = AppSerializerGenerator(app)
        hash = self.write_generator_to_file(self.test_app_str.filename, app_serializers)
        if app_name == 'example.servers':
            self.assertEqual('dccc94d94b0ca509032d70a2670f2693279bd148', hash)
        else:
            self.assertEqual(hash, 'e2ee40dfc4ed435dd701e29548edfa31288604af')
