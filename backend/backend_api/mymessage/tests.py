from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

class MyMessageViewTests(APITestCase):
    def setUp(self):
        self.client = APIClient()

    def test_get_with_message(self):
        url = reverse('mymessage')  # name from your urls.py
        response = self.client.get(url, {'msg': 'Hello'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {'message': 'Hello brrr!'})

    def test_get_without_message(self):
        url = reverse('mymessage')  # name from your urls.py
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {'error': 'No message parameter provided'})
