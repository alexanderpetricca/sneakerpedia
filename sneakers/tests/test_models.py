from django.test import TestCase

from sneakers.models import Sneaker, Brand


class SneakerModelTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.brand = Brand.objects.create(
            name = 'Test Brand',
            description = 'An interesting description of the brand.',
            country = 'United Kingdom',
            year_founded = 2025,
        )

        cls.sneaker = Sneaker.objects.create(
            brand = cls.brand,
            name = 'Test Sneaker',
            summary = 'A useful summary of the sneaker.',
            designer = 'Test Designer',
            year_released = 2025,
            primary_image = 'test_image.jpg',
        )


    def test_brand_model(self):
        """
        Asserts Brand objects are created correctly.
        """
        
        self.assertIsNotNone(self.brand.id)
        self.assertIsNotNone(self.brand.created_at)
        self.assertEqual(self.brand.name, 'Test Brand')
        self.assertEqual(self.brand.description, 'An interesting description of the brand.')
        self.assertEqual(self.brand.country, 'United Kingdom')
        self.assertEqual(self.brand.year_founded, 2025)


    def test_brand_str_method(self):
        """
        Tests brand str method.
        """
        
        self.assertEqual(str(self.brand), 'Test Brand')


    def test_sneaker_model(self):
        """
        Asserts Sneaker objects are created correctly.
        """        
        
        self.assertIsNotNone(self.sneaker.id)
        self.assertIsNotNone(self.sneaker.created_at)
        self.assertEqual(self.sneaker.brand, self.brand)
        self.assertEqual(self.sneaker.name, 'Test Sneaker')
        self.assertEqual(self.sneaker.summary, 'A useful summary of the sneaker.')
        self.assertEqual(self.sneaker.designer, 'Test Designer')
        self.assertEqual(self.sneaker.year_released, 2025)
        self.assertEqual(self.sneaker.primary_image, 'test_image.jpg')


    def test_sneaker_str_method(self):
        """
        Tests sneaker str method.
        """
        
        self.assertEqual(str(self.sneaker), 'Test Sneaker')        