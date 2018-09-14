import stripe
from django.test import TestCase
from django.urls import reverse

from .models import User


class TestHomePageViews(TestCase):

    def test_home_page_loads_correct_template(self):
        response = self.client.get('')
        self.assertTemplateUsed(response, 'home.html')

    def test_default_url_status_code_is_200(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)


class TestLogoutViewWhileLoggedIn(TestCase):

    def setUp(self):
        User.objects.create_user(email='test@gmail.com', full_name='testable full_name', password='testing_test_pw')
        self.client.login(email='test@gmail.com', password='testing_test_pw')

    def test_logged_in_user_loads_correct_template(self):
        response = self.client.get(reverse('logout'))
        self.assertTemplateUsed(response, 'logout.html')


class TestSignUpViewWhileLoggedIn(TestCase):

    def setUp(self):
        User.objects.create_user(email='test@gmail.com', full_name='testable full_name', password='testing_test_pw')
        self.client.login(email='test@gmail.com', password='testing_test_pw')

    def test_logged_in_user_redirects_on_signup_view(self):
        response = self.client.get(reverse('signup'))
        self.assertEqual(response.status_code, 302)


class TestSignUpViewWhileLoggedOut(TestCase):

    def test_signup_view_form_completed(self):
        response = self.client.post(reverse('signup'), data={
            'email': 'test_signupform@gmail.com',
            'full_name': 'test signupform',
            'password1': 'testing_test_pw',
            'password2': 'testing_test_pw'
        })
        self.assertRedirects(response, reverse('home'))
