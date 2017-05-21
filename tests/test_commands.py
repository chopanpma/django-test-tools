
from unittest.mock import Mock, patch

from django.core.management import call_command
from django.db.models import Field
from django.db.models import FileField
from django.test import TestCase

from django_test_tools.file_utils import hash_file
from django_test_tools.management.commands.generate_factories import ModelFactoryGenerator
from django_test_tools.mixins import TestCommandMixin, TestOutputMixin
from django_test_tools.utils import create_output_filename_with_date


class TestGenerateFactories(TestOutputMixin, TestCommandMixin, TestCase):

    def test_generate(self):
        call_command('generate_factories', 'example.my_app', stdout=self.content)
        results = self.get_results()
        self.assertEqual(44, len(results))
        filename = create_output_filename_with_date('example_my_app_factory.py')
        with open(filename, 'w', encoding='utf-8') as factory_file:
            for line in results:
                factory_file.write(line)
                factory_file.write('\n')
        hash_sha = hash_file(filename, algorithm='sha256')
        self.assertEqual('2d3dcb11f945f9d93985c9ee142a0251474002cb19dc7ec92eb5e16e5885c2ac', hash_sha)
        self.clean_output_folder(filename)


class FileFieldMockType(object):
    field_name = None

    # noinspection PyShadowingBuiltins
    def __init__(cls, what, bases=None, dict=None):
        cls.__name__ = 'FileField'


class TestModelFactoryGenerator(TestCase):

    def test__generate_file_field(self):
        field = Mock(spec=FileField)
        field.name = 'hola'
        #self.assertEqual('', type(field).__name__)
        mock_model = Mock()
        mock_model.__name__ = 'SuperModel'
        mock_model._meta = Mock()
        mock_model._meta.fields = [field]
        factory_gen = ModelFactoryGenerator(mock_model)

        with patch('builtins.type', FileFieldMockType) as m_type:
            results = factory_gen._generate()
            field_definition = results[1]['print'].format(*results[1]['args'])
            self.assertEqual('    hola = FileField(filename=\'hola.xlsx\')', field_definition)
            self.assertEqual('    {} = FileField(filename=\'{}.{}\')', results[1]['print'])
            self.assertEqual(['hola', 'hola', 'xlsx'], results[1]['args'])
