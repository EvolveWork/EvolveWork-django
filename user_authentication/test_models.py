from django.test import TestCase

from .models import User, CustomUserManager


class TestUserModel(TestCase):

    def test_string_representation_of_user_model(self):
        entry = User(email='test@gmail.com', full_name='testable full_name')
        self.assertEqual(str(entry), entry.email)

    def test_user_model_get_full_name_method(self):
        entry = User(email='test@gmail.com', full_name='testable full_name')
        self.assertEqual(entry.get_full_name(), 'testable full_name')

    def test_user_model_get_full_name_method_returning_email(self):
        entry = User(email='test@gmail.com')
        self.assertEqual(entry.get_full_name(), 'test@gmail.com')

    def test_user_model_get_short_name_method(self):
        entry = User(email='test@gmail.com', full_name='testable full_name')
        self.assertEqual(entry.get_short_name(), 'testable')

    def test_user_model_get_short_name_method_returning_email(self):
        entry = User(email='test@gmail.com', full_name='testablefull_name')
        self.assertEqual(entry.get_short_name(), 'test@gmail.com')

    def test_has_perm(self):
        entry = User(email='test@gmail.com', full_name='testable full_name')
        self.assertTrue(entry.has_perm(perm='test'))

    def test_has_module_perms(self):
        entry = User(email='test@gmail.com', full_name='testable full_name')
        self.assertTrue(entry.has_module_perms(app_label='test'))

    def test_is_staff(self):
        entry = User(email='test@gmail.com', full_name='testable full_name', staff=True)
        self.assertTrue(entry.is_staff)

    def test_is_admin(self):
        entry = User(email='test@gmail.com', full_name='testable full_name', admin=True)
        self.assertTrue(entry.is_admin)


class TestCustomUserManager(TestCase):

    def test_create_user_password_value_error(self):
        self.assertRaises(ValueError, CustomUserManager.create_user, self, email='test@gmail.com',
                          full_name='testable full_name')

    def test_create_user_email_value_error(self):
        self.assertRaises(ValueError, CustomUserManager.create_user, self, email=None, full_name='testable full_name',
                          password='testable_test_pw')

    def test_create_user_full_name_value_error(self):
        self.assertRaises(ValueError, CustomUserManager.create_user, self, email='test@gmail.com', full_name=None,
                          password='testable_test_pw')

    def test_create_staffuser(self):
        user = User.objects.create_staffuser(email='test@gmail.com', full_name='testable full_name',
                                                  password='testable_test_pw')
        self.assertTrue(user.is_staff)
