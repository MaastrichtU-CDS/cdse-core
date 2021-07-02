from django.test import TestCase


class SanityTestCase(TestCase):

    def test_if_tests_are_run(self):
        number = 1
        self.assertEqual(number, 1)
