import os
import time
import django
import unittest

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

# django.setup() is needed for scripts not served over HTTPS or that weren't ran through manage.py
# in order to access user_authentication.models
django.setup()

from user_authentication.models import User


class UserTestsWhileLoggedOut(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Chrome(os.environ.get('CHROMEDRIVER'))

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
        time.sleep(1)
        user = User.objects.get(email='testoroony@gmail.com')
        self.assertEqual(user.email, 'testoroony@gmail.com')
        user.delete()

    # def test_user_login(self):
    #     user = User.objects.all().filter(email='testoroony@gmail.com')
    #     self.user.login()
    #     # User is logged in
    #     self.assertTrue()

        # Logged in view shows additional options - reset password, unsubscribe

        self.fail('Finish the Logged Out tests.')


if __name__ == '__main__':
    unittest.main(warnings='ignore')
