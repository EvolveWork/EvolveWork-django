from django.test import TestCase
from django.urls import reverse


class HomePageViewTests(TestCase):

    def test_home_page_uses_correct_template(self):
        response = self.client.get('')
        self.assertTemplateUsed(response, 'home.html')

    def test_default_url_status_code_is_200(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

