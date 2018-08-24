from django.test import TestCase
from django.urls import reverse

from user_authentication.models import User


class TestChargeSuccessView(TestCase):

    def setUp(self):
        User.objects.create_user(email='test@gmail.com', full_name='testable full_name', password='testing_test_pw')
        self.client.login(email='test@gmail.com', password='testing_test_pw')

    def test_charge_success_view_loads_correct_template(self):
        response = self.client.get(reverse('charge_success'))
        self.assertTemplateUsed(response, 'charge_success.html')


