import datetime

import stripe
from django.test import TestCase
from django.urls import reverse
from stripe.error import CardError

from evolve_work import settings
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
        User.objects.create_user(email='test@gmail.com', full_name='testable full_name', password='testing_test_pw')
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

    def test_charge_checkout_view(self):

        stripe.api_key = settings.STRIPE_SECRET_KEY

        try:
            token = stripe.Token.create(
                card={
                    'number': '4242424242424242',
                    'exp_month': '6',
                    'exp_year': str(datetime.datetime.today().year + 1),
                    'cvc': '123',
                }
            )
            response = self.client.post(reverse('checkout'), data={
                'stripeToken': token.id,
            })
            self.assertEqual(response.status_code, 302)
            self.assertEqual(response.url, '/charge/success/')

        except Exception:
            self.fail('Stripe api may be down.')


class TestCancelSubscription(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(email='test@gmail.com', full_name='testable full_name',
                                             password='testing_test_pw')
        self.client.login(email='test@gmail.com', password='testing_test_pw')

    def test_cancel_subscription_template(self):
        response = self.client.get(reverse('cancel_subscription'))
        self.assertTemplateUsed(response, 'charge_cancel.html')

    def test_post_to_charge_cancel_complete(self):
        stripe.api_key = settings.STRIPE_SECRET_KEY
        user = User.objects.all().get(email='test@gmail.com')
        user.stripeId = 'cus_DYsX3magOetnyJ'
        user.save()

        response = self.client.get(reverse('cancel_subscription_complete'))
        self.assertTemplateUsed(response, 'charge_cancel_complete.html')


class FailedTestForNotes(TestCase):

    def test_fail_self(self):
        self.fail('next -- delete stripe user after test')

