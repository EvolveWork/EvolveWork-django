from django.test import TestCase
from django.urls import reverse

from .models import User


class TestUserAuthenticationUrls(TestCase):

    def setUp(self):
        self.user = User.objects.create_superuser(
            email='anothertestoroony@gmail.com',
            full_name='anothertest name',
            password='testing_test_pw'
        )

    def test_uses_home_template(self):
        response = self.client.get(reverse('home'))
        self.assertTemplateUsed(response, 'home.html')

    def test_default_url_status_code_is_200(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_sign_up_url_status_code_is_200(self):
        response = self.client.get(reverse('signup'))
        self.assertEqual(response.status_code, 200)

    def test_login_url_status_code_is_200(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)

    def test_password_change_url_status_code_is_200(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('password_change'))
        self.assertEqual(response.status_code, 200)

    def test_password_change_done_url_status_code_is_200(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('password_change_done'))
        self.assertEqual(response.status_code, 200)

    def test_logout_url_status_code_is_302(self):
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)

    def test_account_url_status_code_is_302(self):
        response = self.client.get(reverse('account'))
        self.assertEqual(response.status_code, 302)

    def test_charge_url_status_code_is_302(self):
        response = self.client.get(reverse('charge'))
        self.assertEqual(response.status_code, 302)

    # def test_password_reset_url_status_code_is_200(self):
    #     response = self.client.get(reverse('password_reset'))
    #     self.assertEqual(response.status_code, 200)
    #
    # def test_password_reset_done_url_status_code_is_200(self):
    #     response = self.client.get(reverse('password_reset_done'))
    #     self.assertEqual(response.status_code, 200)
    #
    # def test_password_reset_confirm_url_status_code_is_200(self):
    #     response = self.client.get(reverse('password_reset_confirm', kwargs={'uidb64': 4, 'token': 4}))
    #     self.assertEqual(response.status_code, 200)
    #
    # def test_password_reset_complete_url_status_code_is_200(self):
    #     response = self.client.get(reverse('password_reset_complete'))
    #     self.assertEqual(response.status_code, 200)
