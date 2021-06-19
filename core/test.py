from django.test import TestCase


class SanityTestCase(TestCase):

    def test_if_tests_are_run(self):
        num = 1
        self.assertEqual(num, 1)

