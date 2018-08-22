from django.test import TestCase

from .models import User


class UserModelTest(TestCase):

    def test_string_representation(self):
        entry = User(email='test@gmail.com', full_name='testable full_name')
        self.assertEqual(str(entry), entry.email)