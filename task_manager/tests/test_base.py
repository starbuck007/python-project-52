"""Base test classes and mixins for task manager app."""
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User


class BaseTestCase(TestCase):
    """Base class for all test cases."""

    def setUp(self):
        """Setup for all tests."""
        self.user = User.objects.create_user(
            username='darth_vader',
            password='123456',
            first_name='Darth',
            last_name='Vader'
        )
        self.user2 = User.objects.create_user(
            username='luke',
            password='54321',
            first_name='Luke',
            last_name='Skywalker'
        )
        self.client = Client()

    def login_user(self):
        """Method to login main user."""
        return self.client.login(username='darth_vader',
                                 password='123456')


class CRUDTestMixin:
    """Mixin with common CRUD test methods."""
    model_class = None
    base_url_name = None
    create_data = {}
    update_data = {}

    def test_list_view(self):
        """List view returns correct response."""
        self.login_user()
        response = self.client.get(reverse(f'{self.base_url_name}_list'))
        self.assertEqual(response.status_code, 200)

    def test_create_view(self):
        """Test creating a new object."""
        self.login_user()
        response = self.client.post(
            reverse(f'{self.base_url_name}_create'),
            self.create_data,
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            self.model_class.objects.filter(**self.create_data).exists())

    def test_update_view(self):
        """Test updating an existing object."""
        self.login_user()
        obj = self.model_class.objects.first()
        response = self.client.post(
            reverse(f'{self.base_url_name}_update', kwargs={'pk': obj.pk}),
            self.update_data,
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        obj.refresh_from_db()
        for key, value in self.update_data.items():
            self.assertEqual(getattr(obj, key), value)

    def test_delete_view(self):
        """Test deleting an object."""
        self.login_user()
        obj = self.model_class.objects.first()
        obj_pk = obj.pk
        response = self.client.post(
            reverse(f'{self.base_url_name}_delete', kwargs={'pk': obj_pk}),
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertFalse(self.model_class.objects.filter(pk=obj_pk).exists())

    def test_unauthorized_access(self):
        """Unauthorized access redirects login page."""
        self.client.logout()
        obj = self.model_class.objects.first()
        urls = [
            reverse(f'{self.base_url_name}_list'),
            reverse(f'{self.base_url_name}_create'),
            reverse(f'{self.base_url_name}_update', kwargs={'pk': obj.pk}),
            reverse(f'{self.base_url_name}_delete', kwargs={'pk': obj.pk})
        ]
        for url in urls:
            response = self.client.get(url)
            self.assertEqual(response.status_code, 302)
            self.assertTrue(response.url.startswith(reverse('login')))
