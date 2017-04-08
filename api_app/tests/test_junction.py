from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from api_app.models import Junction

class JunctionTests(APITestCase):
    def test_create_junction(self):
        """
        Test adding a new junction."
        """
        url = reverse('junction-list')
        data = {'description': 'Test junction'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Junction.objects.count(), 1)
        self.assertEqual(Junction.objects.get().description, 'Test junction')

    def test_duplicate_junction(self):
        """
        Test that adding a junction with an existing description fails."
        """
        url = reverse('junction-list')
        data = {'description': 'Test junction'}
        response = self.client.post(url, data, format='json')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Junction.objects.count(), 1)

