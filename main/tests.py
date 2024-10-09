# Create your tests here.
from django.test import TestCase, Client

class TestViews(TestCase):
    def test_main(self):
        client = Client()
        response = client.get('/')
        self.assertEqual(response.status_code, 200)