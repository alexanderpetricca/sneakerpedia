from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from sneakers.models import Brand, Sneaker


class BrandAPITests(APITestCase):
    """
    Tests for the Brand API endpoints.
    """

    def setUp(self):
        """
        Set up initial data for the tests.
        """
        
        self.brand1 = Brand.objects.create(
            name='Brand A', 
            description='First brand.',
        )
        self.brand2 = Brand.objects.create(
            name='Brand B', 
            description='Second brand.',
        )
        self.sneaker1 = Sneaker.objects.create(
            brand=self.brand1, 
            name='Sneaker 1A', 
            year_released=2024,
        )
        self.sneaker2 = Sneaker.objects.create(
            brand=self.brand1, 
            name='Sneaker 2A', 
            year_released=2025,
        )
        self.sneaker3 = Sneaker.objects.create(
            brand=self.brand2, 
            name='Sneaker 3B', 
            year_released=2025,
        )


    def test_list_brands(self):
        """
        Ensure we can retrieve a list of all brands.
        """

        url = reverse('brands-list')
        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        brand_names = [item['name'] for item in response.data]
        self.assertIn('Brand A', brand_names)
        self.assertIn('Brand B', brand_names)


    def test_retrieve_brand(self):
        """
        Ensure we can retrieve a single brand by its ID.
        """

        url = reverse('brands-detail', kwargs={'pk': self.brand1.pk})
        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.brand1.name)
        self.assertEqual(response.data['description'], self.brand1.description)


    def test_brand_sneakers_custom_action(self):
        """
        Ensure the custom 'sneakers' action returns the correct sneakers for 
        a brand.
        """

        url = reverse('brands-sneakers', kwargs={'pk': self.brand1.pk})
        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        sneaker_names = [item['name'] for item in response.data]
        self.assertIn('Sneaker 1A', sneaker_names)
        self.assertIn('Sneaker 2A', sneaker_names)
        self.assertNotIn('Sneaker 3B', sneaker_names)


class SneakerAPITests(APITestCase):
    """
    Tests for the Sneaker API endpoints.
    """

    def setUp(self):
        """
        Set up initial data for the tests.
        """
        
        self.brand = Brand.objects.create(
            name='Test Brand',
        )
        self.sneaker1 = Sneaker.objects.create(
            brand=self.brand, 
            name='Test Sneaker 1', 
            year_released=2024,
        )
        self.sneaker2 = Sneaker.objects.create(
            brand=self.brand,
            name='Test Sneaker 2', 
            year_released=2025,
        )


    def test_list_sneakers(self):
        """
        Ensure we can retrieve a list of all sneakers.
        """
        
        url = reverse('sneakers-list')
        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        sneaker_names = [item['name'] for item in response.data]
        self.assertIn('Test Sneaker 1', sneaker_names)


    def test_retrieve_sneaker(self):
        """
        Ensure we can retrieve a single sneaker by its ID.
        """
        
        url = reverse('sneakers-detail', kwargs={'pk': self.sneaker1.pk})
        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.sneaker1.name)
        self.assertEqual(response.data['brand'], self.brand.pk)