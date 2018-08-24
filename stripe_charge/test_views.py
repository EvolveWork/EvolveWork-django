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


class TestCheckoutView(TestCase):

    def setUp(self):
        User.objects.create_user(email='test@gmail.com', full_name='testable full_name', password='testing_test_pw')
        self.client.login(email='test@gmail.com', password='testing_test_pw')

    def test_charge_checkout_view(self):
        response = self.client.post(reverse('signup'), data={
            'stripeToken':'4242424242424242',
            'stripeId': 'cus_DSEvdbRV8IUQC1',
            'stripeBillingAddressLine1': '518 a. North 14th st.',
            'zipCode': '81230',
            'stripeBillingAddressState': 'CO',
            'stripeBillingAddressCity': 'Gunnison',
            'stripeBillingAddressCountry': 'United States'
        })
