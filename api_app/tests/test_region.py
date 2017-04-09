from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from api_app.models import Region

class RegionTests(APITestCase):
    def test_create_region(self):
        """
        Test adding a new region."
        """
        url = reverse('region-list')
        data = {'name': 'Test region'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Region.objects.count(), 1)
        self.assertEqual(Region.objects.get().name, 'Test region')

    def test_duplicate_region(self):
        """
        Test that adding a region with an existing name fails."
        """
        url = reverse('region-list')
        data = {'name': 'Test region'}
        response = self.client.post(url, data, format='json')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Region.objects.count(), 1)

