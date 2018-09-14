import os
import time
import unittest

import django
from django.test import TestCase, Client
from django.urls import reverse
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

# django.setup() is needed for scripts not served over HTTPS or that weren't ran through manage.py
# in order to access user_authentication.models
django.setup()

from user_authentication.models import User


class UserTestsWhileLoggedOutSelenium(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Chrome(os.environ.get('CHROMEDRIVER'))
        self.client = Client()

    def tearDown(self):
        self.browser.quit()

    def test_site_load(self):
        # User goes to site to sign up for a payment plan
        self.browser.get('http://127.0.0.1:8000/')

        # User sees proper title
        self.assertIn('Evolve Coworking', self.browser.title)

        # Page loads with navigation options
        navigation_while_logged_out = self.browser.find_elements_by_class_name('navigation')
        self.assertEqual(len(navigation_while_logged_out), 3)

    def test_user_signup(self):
        # User loads sign up page
        self.browser.get('http://127.0.0.1:8000/signup/')

        # User sees four input fields
        email_input = self.browser.find_element_by_id('id_email')
        full_name_input = self.browser.find_element_by_id('id_full_name')
        password1_input = self.browser.find_element_by_id('id_password1')
        password2_input = self.browser.find_element_by_id('id_password2')
        submit_signup_button = self.browser.find_element_by_id('submit_signup_button')

        # User inputs email, full_name, password1, and password2
        email_input.send_keys('testoroony@gmail.com')
        full_name_input.send_keys('test name')
        password1_input.send_keys('testing_test_pw')
        password2_input.send_keys('testing_test_pw')

        # User is saved to the database
        submit_signup_button.send_keys(Keys.ENTER)

        # Testing on redirect status code after logging in.
        self.client.login(email='testoroony@gmail.com', password='testing_test_pw')
        response = self.client.get(reverse('logout_success'))
        self.assertEqual(response.status_code, 302)

    def test_user_login(self):
        # User loads up login page
        self.browser.get('http://127.0.0.1:8000/login/')

        # User sees two input fields and a submit button
        email_input = self.browser.find_element_by_id('id_username')
        password_input = self.browser.find_element_by_id('id_password')
        submit_login_button = self.browser.find_element_by_id('submit_login_button')

        # User inputs login information
        email_input.send_keys('test@gmail.com')
        password_input.send_keys('testing_test_pw')
        submit_login_button.send_keys(Keys.ENTER)
        time.sleep(1)
        self.client.login(email='test@gmail.com', password='testing_test_pw')

        # Testing on redirect status code after logging in.
        response = self.client.get(reverse('logout_success'))

        self.assertEqual(response.status_code, 302)


class UserTestsWhileLoggedIn(TestCase):
    def setUp(self):
        User.objects.create_user(email='test@gmail.com', full_name='testable full_name', password='testing_test_pw')
        self.client.login(email='test@gmail.com', password='testing_test_pw')

    def test_navigation_options_changed(self):
        # User is logged in when homepage is loaded
        response = self.client.get('/')
        processed_response = response.content.decode()

        # User sees new navigation options
        self.assertIn('<li><a title="Charge" class="navigation" href="/charge/">Subscribe</a></li>',
                      processed_response)
        self.assertIn('<li><a title="Account" class="navigation" href="/account/">Account</a></li>',
                      processed_response)
        self.assertIn('<li><a title="Logout" class="navigation" href="/logout/">Logout</a></li>',
                      processed_response)

    def test_charge_page_loads_stripe_js(self):
        response = self.client.get('/charge/')
        self.assertIn('src="https://checkout.stripe.com/checkout.js"', response.content.decode())


if __name__ == '__main__':
    unittest.main(warnings='ignore')
