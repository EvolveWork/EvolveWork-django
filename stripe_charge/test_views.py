import datetime
from unittest import mock

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
        """These two tests must live together because they need to be done sequentially.

        First, we place a donation using the client. Then we send a mock callback to our
        webhook, to make sure it accepts it properly.
        """
        try:
            stripe.api_key = settings.STRIPE_SECRET_KEY
            token = stripe.Token.create(
                card={
                    'number': '4242424242424242',
                    'exp_month': '6',
                    'exp_year': str(datetime.datetime.today().year + 1),
                    'cvc': '123',
                }
            )

            response = self.client.post(reverse('checkout'), data={
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
            })
            # self.assertTemplateUsed(response, 'charge_success.html')
            self.assertEqual(response.status_code, 302)

        except Exception as e:
            print(e)
            self.fail('Stripe api may be down.')

        # Get the stripe event so we can post it to the webhook
        # We don't know the event ID, so we have to get the latest ones, then filter...
        # events = stripe.Event.all()
        # event = None
        # for obj in events.data:
        #     if obj.data.object.card.fingerprint == token.card.fingerprint:
        #         event = obj
        #         break
        # self.assertIsNotNone(event, msg="Unable to find correct event for token: %s" % token.card.fingerprint)
        #
        # # Finally, we can test the webhook!
        # r = self.client.post('/donate/callbacks/stripe/',
        #                      data=simplejson.dumps(event),
        #                      content_type='application/json')
        #
        # # Does it return properly?
        # self.assertEqual(r.status_code, 200)


class TestCancelSubscription(TestCase):

    def setUp(self):
        User.objects.create_user(email='test@gmail.com', full_name='testable full_name', password='testing_test_pw')
        self.client.login(email='test@gmail.com', password='testing_test_pw')

    def test_cancel_subscription_template(self):
        response = self.client.get(reverse('cancel_subscription'))
        self.assertTemplateUsed(response, 'charge_cancel.html')

    def test_exception_raised(self):
        self.assertRaises(Exception, stripe.Customer.retrieve, stripeId=1)
