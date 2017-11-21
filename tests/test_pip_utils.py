from django.conf import settings
from django.test import SimpleTestCase

from django_test_tools.assert_utils import write_assertions
from django_test_tools.file_utils import temporary_file
from django_test_tools.pip.utils import parse_specifier, read_requirement_file, list_outdated_libraries, \
    update_outdated_libraries


class TestParseSpecifier(SimpleTestCase):

    def test_parse_specifier(self):
        result = parse_specifier('==2.1.1')
        self.assertEqual(result[0], '==')
        self.assertEqual(result[1], '2.1.1')

    def test_parse_specifier(self):
        with self.assertRaises(ValueError) as context:
            parse_specifier('2.1.1')

        self.assertEqual(str(context.exception), 'Invalid speficier "2.1.1"')

    # def test_list_outdated_libraries(self):
    #     outdated = list_outdated_libraries()
    #     #write_assertions(outdated, 'outdated')
    #     self.assertTrue(len(outdated)>0)
    #     self.assertIsNotNone(outdated[0]['current_version'])
    #     self.assertIsNotNone(outdated[0]['name'])
    #     self.assertIsNotNone(outdated[0]['new_version'])


class TestReadRequirementFile(SimpleTestCase):

    def setUp(self):
        self.requirements = list()
        self.requirements.append('django==1.11.3 # pyup: >=1.10,<1.11\n')
        self.requirements.append('celery==4.0.1\n')
        self.requirements.append('redis>=2.10.5\n')

    @temporary_file(extension='txt', delete_on_exit=True)
    def test_update_outdated_libraries(self):
        filename = self.test_update_outdated_libraries.filename
        with open(filename, 'w', encoding='utf-8') as req_file:
            req_file.writelines(self.requirements)
        changes = update_outdated_libraries(filename)
        #write_assertions(changes, 'changes')

    @temporary_file(extension='txt', delete_on_exit=True)
    def test_read_requirement_file(self):
        filename = self.test_read_requirement_file.filename

        with open(filename, 'w', encoding='utf-8') as req_file:
            req_file.writelines(self.requirements)

        requirements = read_requirement_file(filename)
        #write_assertions(requirements, 'requirements')
        self.assertEqual(requirements['celery']['comes_from']['file_indicator'], '-r')
        self.assertTrue(filename in requirements['celery']['comes_from']['filename'])
        self.assertEqual(requirements['celery']['comes_from']['line_no'], 2)
        self.assertTrue(filename in requirements['celery']['comes_from']['value'])
        self.assertEqual(requirements['celery']['name'], 'celery')
        self.assertEqual(requirements['celery']['operator'], '==')
        self.assertEqual(requirements['celery']['version'], '4.0.1')
        self.assertEqual(requirements['django']['comes_from']['file_indicator'], '-r')
        self.assertTrue(filename in requirements['django']['comes_from']['filename'])
        self.assertEqual(requirements['django']['comes_from']['line_no'], 1)
        self.assertTrue(filename in requirements['django']['comes_from']['value'])
        self.assertEqual(requirements['django']['name'], 'django')
        self.assertEqual(requirements['django']['operator'], '==')
        self.assertEqual(requirements['django']['version'], '1.11.3')
        self.assertEqual(requirements['redis']['comes_from']['file_indicator'], '-r')
        self.assertTrue(filename in requirements['redis']['comes_from']['filename'])
        self.assertEqual(requirements['redis']['comes_from']['line_no'], 3)
        self.assertTrue(filename in requirements['redis']['comes_from']['value'])
        self.assertEqual(requirements['redis']['name'], 'redis')
        self.assertEqual(requirements['redis']['operator'], '>=')
        self.assertEqual(requirements['redis']['version'], '2.10.5')

