from django.test import TestCase

from .models import User


class UserModelTest(TestCase):

    def test_string_representation_of_user_model(self):
        entry = User(email='test@gmail.com', full_name='testable full_name')
        self.assertEqual(str(entry), entry.email)

    def test_user_model_get_full_name_method(self):
        entry = User(email='test@gmail.com', full_name='testable full_name')
        self.assertEqual(entry.get_full_name(), 'testable full_name')
