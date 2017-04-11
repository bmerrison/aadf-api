from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from api_app.models import Region, LocalAuthority
from test_util import login

class RegionTests(APITestCase):
    def test_create_region(self):
        """
        Test adding a new region."
        """
        login(self.client)
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
        login(self.client)
        url = reverse('region-list')
        data = {'name': 'Test region'}
        response = self.client.post(url, data, format='json')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Region.objects.count(), 1)

    def test_create_local_authority(self):
        """
        Test adding a new local authority."
        """
        login(self.client)
        url = reverse('region-list')
        data = {'name': 'Test region'}
        response = self.client.post(url, data, format='json')
        region_id = response.json()['id']

        url = reverse('localauthority-list')
        data = {'name': 'Test local authority',
                'region': region_id}

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(LocalAuthority.objects.count(), 1)
        self.assertEqual(LocalAuthority.objects.get().name, 'Test local authority')
        self.assertEqual(LocalAuthority.objects.get().region.name, 'Test region')

    def test_duplicate_local_authority(self):
        """
        Test adding local authorities with duplicate names. Should be
        allowed as long as they're in different regions.
        """
        login(self.client)
        # Create a couple of regions.
        url = reverse('region-list')
        data = {'name': 'Test region 1'}
        response = self.client.post(url, data, format='json')
        region1_id = response.json()['id']
        data = {'name': 'Test region 2'}
        response = self.client.post(url, data, format='json')
        region2_id = response.json()['id']

        # Add first two authorities in different regions (should work).
        url = reverse('localauthority-list')
        data = {'name': 'Test local authority',
                'region': region1_id}
        response = self.client.post(url, data, format='json')
        data = {'name': 'Test local authority',
                'region': region2_id}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(LocalAuthority.objects.count(), 2)

        # Add another in the same region as the second. Should fail.
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(LocalAuthority.objects.count(), 2)
   

