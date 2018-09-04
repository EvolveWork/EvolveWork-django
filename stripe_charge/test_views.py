import datetime
from unittest import mock

import stripe
from stripe.api_resources import Token
from django.test import TestCase
from django.urls import reverse
from stripe.error import CardError

from stripe_charge.models import MockCustomer, MockToken
from user_authentication.models import User


class TestChargeSuccessView(TestCase):

    def setUp(self):
        User.objects.create_user(email='test@gmail.com', full_name='testable full_name', password='testing_test_pw')
        self.client.login(email='test@gmail.com', password='testing_test_pw')

    def test_charge_success_view_loads_correct_template(self):
        response = self.client.get(reverse('charge_success'))
        self.assertTemplateUsed(response, 'charge_success.html')


class TestCheckoutViewLoggedOut(TestCase):
    def test_checkout_view(self):
        response = self.client.get(reverse('checkout'))
        self.assertEqual(response.status_code, 302)


class TestCheckoutView(TestCase):

    def setUp(self):
        User.objects.create_user(email='test10@gmail.com', full_name='testable full_name', password='testing_test_pw')
        self.client.login(email='test@gmail.com', password='testing_test_pw')

    def test_checkout_with_incorrect_card(self):
        try:
            self.assertRaises(stripe.error.CardError, stripe.Token.create, card={
                'number': '4242424242424241',
                'exp_month': '6',
                'exp_year': str(datetime.datetime.today().year + 1),
                'cvc': '123',
            })
        except Exception:
            self.fail('Stripe api may be down.')

    @mock.patch('stripe.Token', MockToken)
    @mock.patch('stripe.Customer.create', MockCustomer)
    def test_stripe_create_customer(self, mock_create):

        token = stripe.Token.create(
            card={
                'number': '4242424242424242',
                'exp_month': '6',
                'exp_year': str(datetime.datetime.today().year + 1),
                'cvc': '123',
            }
        )

        data = {
            'amount': '25',
            'payment_provider': 'cc',
            'first_name': 'Barack',
            'last_name': 'Obama',
            'address1': '1600 Pennsylvania Ave.',
            'address2': 'The Whitehouse',
            'city': 'DC',
            'state': 'DC',
            'zip_code': '20500',
            'email': 'barack@freelawproject.org',
            'referrer': 'footer',
            'stripeToken': token.id,
        }

        response = self.client.post(reverse('checkout'), data=data, format='json')
        self.assertEqual(response.status_code, 302)

    # def test_charge_checkout_view(self):
    #
    #     # TODO - Need to be sure that the proper template/redirection is occuring.
    #
    #     try:
    #         token = stripe.Token.create(
    #             card={
    #                 'number': '4242424242424242',
    #                 'exp_month': '6',
    #                 'exp_year': str(datetime.datetime.today().year + 1),
    #                 'cvc': '123',
    #             }
    #         )
    #         response = self.client.post(reverse('checkout'), data={
    #             'amount': '25',
    #             'payment_provider': 'cc',
    #             'first_name': 'Barack',
    #             'last_name': 'Obama',
    #             'address1': '1600 Pennsylvania Ave.',
    #             'address2': 'The Whitehouse',
    #             'city': 'DC',
    #             'state': 'DC',
    #             'zip_code': '20500',
    #             'email': 'barack@freelawproject.org',
    #             'referrer': 'footer',
    #             'stripeToken': token.id,
    #         })
    #         self.assertEqual(response.status_code, 302)
    #
    #     except Exception:
    #         self.fail('Stripe api may be down.')


class TestCancelSubscription(TestCase):

    def setUp(self):
        User.objects.create_user(email='test@gmail.com', full_name='testable full_name', password='testing_test_pw')
        self.client.login(email='test@gmail.com', password='testing_test_pw')

    def test_cancel_subscription_template(self):
        response = self.client.get(reverse('cancel_subscription'))
        self.assertTemplateUsed(response, 'charge_cancel.html')

    def test_exception_raised(self):
        self.assertRaises(Exception, stripe.Customer.retrieve, stripeId=1)
