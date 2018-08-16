import os

from selenium import webdriver
import unittest


class UserTests(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Chrome(os.environ.get('CHROMEDRIVER'))

    def tearDown(self):
        self.browser.quit()

    def test_site_load(self):
        # User goes to site to sign up for a payment plan
        self.browser.get('http://127.0.0.1:8000/')

        # User sees evolve work in title
        assert 'evolve work' in self.browser.title

        # Page loads with plans
        plans = self.browser.find_elements_by_class_name('plans')
        print(plans[0].get_attribute('placeholder'))
        # print(plans[0])
        # assert ['Day', 'Month', '6-month', '12-month'] in plans
        # User clicks the plan they want (Daily, Monthly, 6-month, 12-month)


# Plan is loaded - 'Pay with card' represents plan the User wants


# User inputs information that is then sent to Stripe.


# Database stores information that Stripe reports (name, email, address, plan)


#

if __name__ == '__main__':
    unittest.main(warnings='ignore')
