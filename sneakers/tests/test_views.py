import tempfile

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.contrib.auth.models import Permission
from django.core.files.uploadedfile import SimpleUploadedFile

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


class SneakerManageViewTests(TestCase):
    
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            email="testuser@email.com",
            first_name="Test",
            last_name="User",
            password="testpass123",
        )

        cls.brand = Brand.objects.create(
            name='Test Brand',
            description='An interesting desciption of the brand.',
            country='United Kingdom',
            year_founded=2025,
        )

        cls.add_sneaker = Permission.objects.get(codename='add_sneaker')
        cls.change_sneaker = Permission.objects.get(codename='change_sneaker')
        cls.delete_sneaker = Permission.objects.get(codename='delete_sneaker')


    def setUp(self):
        """
        This method runs before every test.
        Use it to create objects that interact with the filesystem.
        """

        dummy_image = SimpleUploadedFile(
            "test_image.jpg", 
            b"file contents for a sneaker",
            "image/jpeg"
        )
        
        self.sneaker = Sneaker.objects.create(
            brand=self.brand,
            name='Test Sneaker',
            summary='A useful summary of sneaker.',
            designer='Test Designer',
            year_released=2025,
            primary_image=dummy_image,
        )        
        

    # CREATE
    def test_create_sneaker_view_logged_out(self):
        """
        Tests redirect to login when accessing create sneaker page while logged out.
        """

        self.client.logout()
        url = reverse('create_sneaker')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f"{reverse('account_login')}?next={url}")
        response = self.client.get(f"{reverse('account_login')}?next={url}")
        self.assertTemplateUsed(response, 'account/login.html')


    def test_create_sneaker_view_logged_in_no_perm(self):
        """
        Tests 403 if user is logged in without permission and tries to access create sneaker page.
        """

        self.client.login(email="testuser@email.com", password="testpass123")
        url = reverse('create_sneaker')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 403)


    def test_create_sneaker_view_logged_in_with_perm(self):
        """
        Tests create sneaker page loads and POST creates sneaker if user has permission.
        """

        self.user.user_permissions.add(self.add_sneaker)
        self.client.login(email="testuser@email.com", password="testpass123")
        url = reverse('create_sneaker')
        
        # GET
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        new_image = SimpleUploadedFile(
            "updated_image.jpg", 
            b"new content", 
            "image/jpeg"
        )
        
        # POST
        data = {
            'brand': self.brand.id,
            'name': 'New Sneaker',
            'summary': 'A new sneaker summary.',
            'designer': 'New Designer',
            'year_released': 2024,
            'primary_image': new_image,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Sneaker.objects.filter(name='New Sneaker').exists())


    # UPDATE
    def test_update_sneaker_view_logged_out(self):
        """
        Tests redirect to login when accessing update sneaker page while logged out.
        """

        self.client.logout()
        url = reverse('update_sneaker', kwargs={'pk': self.sneaker.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f"{reverse('account_login')}?next={url}")
        response = self.client.get(f"{reverse('account_login')}?next={url}")
        self.assertTemplateUsed(response, 'account/login.html')


    def test_update_sneaker_view_logged_in_no_perm(self):
        """
        Tests 403 if user is logged in without permission and tries to access update sneaker page.
        """

        self.client.logout()
        self.client.login(email="testuser@email.com", password="testpass123")
        url = reverse('update_sneaker', kwargs={'pk': self.sneaker.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)


    def test_update_sneaker_view_logged_in_with_perm(self):
        """
        Tests update sneaker page loads and POST updates sneaker if user has permission.
        """

        self.user.user_permissions.add(self.change_sneaker)
        self.client.login(email="testuser@email.com", password="testpass123")
        url = reverse('update_sneaker', kwargs={'pk': self.sneaker.id})
        
        # GET
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        
        updated_image = SimpleUploadedFile(
            "updated_image.jpg", 
            b"new content", 
            "image/jpeg"
        )
        
        # POST
        data = {
            'brand': self.brand.id,
            'name': 'Updated Sneaker',
            'summary': 'Updated summary.',
            'designer': 'Updated Designer',
            'year_released': 2024,
            'primary_image': updated_image,
        }

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.sneaker.refresh_from_db()
        self.assertEqual(self.sneaker.name, 'Updated Sneaker')
        self.assertEqual(self.sneaker.summary, 'Updated summary.')


    # DELETE
    def test_delete_sneaker_view_logged_out(self):
        """
        Tests redirect to login when accessing delete sneaker page while logged out.
        """

        self.client.logout()
        url = reverse('delete_sneaker', kwargs={'pk': self.sneaker.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f"{reverse('account_login')}?next={url}")
        response = self.client.get(f"{reverse('account_login')}?next={url}")
        self.assertTemplateUsed(response, 'account/login.html')


    def test_delete_sneaker_view_logged_in_no_perm(self):
        """
        Tests 403 if user is logged in without permission and tries to access delete sneaker page.
        """

        self.client.logout()
        self.client.login(email="testuser@email.com", password="testpass123")
        url = reverse('delete_sneaker', kwargs={'pk': self.sneaker.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)


    def test_delete_sneaker_view_logged_in_with_perm(self):
        """
        Tests delete sneaker page loads and POST deletes sneaker if user has permission.
        """
        self.user.user_permissions.add(self.delete_sneaker)
        self.client.login(email="testuser@email.com", password="testpass123")
        url = reverse('delete_sneaker', kwargs={'pk': self.sneaker.id})

        # GET
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        # POST
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        
        self.sneaker.refresh_from_db()        
        self.assertIsNotNone(self.sneaker.deleted)