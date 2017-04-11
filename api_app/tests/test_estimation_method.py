from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from api_app.models import Junction, EstimationMethod
from test_util import login
class EstimationMethodTests(APITestCase):
    def test_create_estimation_method(self):
        """
        Test adding a new estimation method."
        """
        login(self.client)
        url = reverse('estimationmethod-list')
        data = {'description': 'Test estimation method'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(EstimationMethod.objects.count(), 1)
        self.assertEqual(EstimationMethod.objects.get().description, 'Test estimation method')

    def test_duplicate_estimation_method(self):
        """
        Test that adding an estimation method with an existing description fails."
        """
        login(self.client)
        url = reverse('estimationmethod-list')
        data = {'description': 'Test estimation method'}
        response = self.client.post(url, data, format='json')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(EstimationMethod.objects.count(), 1)


