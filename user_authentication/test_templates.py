import os

from django.test import TestCase
from selenium import webdriver


# class BaseTemplateTests(TestCase):
#     def setUp(self):
#         self.browser = webdriver.Chrome(os.environ.get('CHROMEDRIVER'))
#
#     def tearDown(self):
#         self.browser.quit()
#
#     def test_site_load(self):
#         self.client.login(email='test@gmail.com', password='testing_test_pw')
#         response = self.client.get('/')
#         self.assertIn('<li><a title="Charge" class="navigation" href="/charge/">Subscribe</a></li>',
#                       response.content.decode())
