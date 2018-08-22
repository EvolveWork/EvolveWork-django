from django.test import TestCase

from .forms import SignupForm


class SignUpFormTest(TestCase):

    def test_valid_data_in_SignUpForm(self):
        form = SignupForm({
            'email': 'test_signupform@gmail.com',
            'full_name': 'test signupform',
            'password1': 'testing_test_pw',
            'password2': 'testing_test_pw'
        })
        self.assertTrue(form.is_valid())
        user = form.save()
        self.assertEqual(user.email, 'test_signupform@gmail.com')
        self.assertEqual(user.full_name, 'test signupform')

    def test_blank_data_in_SignUpForm(self):
        form = SignupForm({})
        self.assertFalse(form.is_valid())

