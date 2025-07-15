from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from sneakers.models import Sneaker, Brand


class SneakerViewTests(TestCase):

    @classmethod
    def setUpTestData(cls):

        cls.user = get_user_model().objects.create_user(
            email = "testuser@email.com",
            first_name = "Test",
            last_name = "User",          
            password = "testpass123",
        )

        cls.brand = Brand.objects.create(
            name = 'Test Brand',
            description = 'An interesting desciption of the brand.',
            country = 'United Kingdom',
            year_founded = 2025,
        )

        cls.sneaker = Sneaker.objects.create(
            brand = cls.brand,
            name = 'Test Sneaker',
            summary = 'A useful summary of sneaker.',
            designer = 'Test Designer',
            year_released = 2025,
            primary_image = 'test_image.jpg',
        )
        
        
    def test_home_page_view(self):
        """
        Tests homepage view functionality.
        """

        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Brand')
        self.assertContains(response, 'Test Sneaker')


    def test_query_view_no_query(self):
        """
        Tests query view functionality.
        """

        response = self.client.get(reverse('query'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Brand')
        self.assertContains(response, 'Test Sneaker')


    def test_query_view_with_search_param(self):
        """
        Tests query view functionality, with an search parameter.
        """        
        
        response = self.client.get(f'{reverse('query')}?search=Test+Sneaker')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Brand')
        self.assertContains(response, 'Test Sneaker')         


    def test_detail_view(self):
        """
        Tests detail view functionality.
        """        
        
        response = self.client.get(reverse('detail', kwargs={'pk': self.sneaker.id}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Brand')
        self.assertContains(response, 'Test Sneaker')