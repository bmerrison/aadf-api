from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from api_app.models import Road, RoadCategory
from test_util import login

class RegionTests(APITestCase):
    def test_create_road(self):
        """
        Test adding a new road."
        """
        login(self.client)
        # Add a category first (should be separate test?)
        url = reverse('roadcategory-list')
        data = {'code': 'PM',
                'description': 'M or Class A Principal Motorway'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(RoadCategory.objects.count(), 1)
        self.assertEqual(RoadCategory.objects.get().code, 'PM')
        self.assertEqual(RoadCategory.objects.get().description, 'M or Class A Principal Motorway')
        cat_id = RoadCategory.objects.get().id

        # Now add road.
        url = reverse('road-list')
        data = {'name': 'TESTROAD',
                'category': cat_id}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Road.objects.count(), 1)
        self.assertEqual(Road.objects.get().name, 'TESTROAD')
        self.assertEqual(Road.objects.get().category.id, cat_id)

    def test_create_duplicate_roads(self):
        """
        Test adding roads with duplicate names. Should be allowed if category is different."
        """
        login(self.client)
        # Create a couple of categories.
        url = reverse('roadcategory-list')
        data = {'code': 'PM',
                'description': 'M or Class A Principal Motorway'}
        response = self.client.post(url, data, format='json')
        cat1_id = RoadCategory.objects.get(code='PM').id
        data = {'code': 'PR',
                'description': 'Class A Principal road in Rural area '}
        response = self.client.post(url, data, format='json')
        cat2_id = RoadCategory.objects.get(code='PR').id

        # Add two roads with the same name but different categories (should work).
        url = reverse('road-list')
        data = {'name': 'TESTROAD',
                'category': cat1_id}
        response = self.client.post(url, data, format='json')
        data = {'name': 'TESTROAD',
                'category': cat2_id}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Road.objects.count(), 2)

        # Add another road with the same name and category (should fail).
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Road.objects.count(), 2)

        
