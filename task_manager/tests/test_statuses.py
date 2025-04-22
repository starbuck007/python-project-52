"""test_statuses.py module for the task manager app."""
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from task_manager.statuses.models import Status


class StatusTestCase(TestCase):
    """Class representing StatusTestCase logic."""
    def setUp(self):
        """Handles the setUp view logic."""
        self.user = User.objects.create_user(
            username='dark_lord',
            password='strongpassword123',
            first_name='Darth',
            last_name='Vader'
        )
        self.status = Status.objects.create(name='Test Status')
        self.client = Client()

    def test_statuses_list(self):
        """Handles the test_statuses_list view logic."""
        self.client.login(username='dark_lord', password='strongpassword123')
        response = self.client.get(reverse('status_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'statuses/statuses.html')
        self.assertContains(response, 'Test Status')

    def test_status_create(self):
        """Handles the test_status_create view logic."""
        self.client.login(username='dark_lord', password='strongpassword123')
        response = self.client.post(
            reverse('status_create'),
            {'name': 'Test Status 2'}
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Status.objects.filter(name='Test Status 2').exists())

    def test_status_create_duplicate(self):
        """Handles the test_status_create_duplicate view logic."""
        self.client.login(username='dark_lord', password='strongpassword123')
        self.client.post(
            reverse('status_create'),
            {'name': 'Test Status'}
        )
        self.assertEqual(Status.objects.filter(name='Test Status').count(), 1)

    def test_status_update(self):
        """Handles the test_status_update view logic."""
        self.client.login(username='dark_lord', password='strongpassword123')
        response = self.client.post(
            reverse('status_update', kwargs={'pk': self.status.pk}),
            {'name': 'Updated Status'}
        )
        self.assertEqual(response.status_code, 302)
        self.status.refresh_from_db()
        self.assertEqual(self.status.name, 'Updated Status')

    def test_status_delete(self):
        """Handles the test_status_delete view logic."""
        self.client.login(username='dark_lord', password='strongpassword123')
        response = self.client.post(
            reverse('status_delete', kwargs={'pk': self.status.pk})
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Status.objects.filter(pk=self.status.pk).exists())

    def test_status_unauthorized_access(self):
        """Handles the test_status_unauthorized_access view logic."""
        urls = [
            reverse('status_list'),
            reverse('status_create'),
            reverse('status_update', kwargs={'pk': self.status.pk}),
            reverse('status_delete', kwargs={'pk': self.status.pk})
        ]
        for url in urls:
            response = self.client.get(url)
            self.assertEqual(response.status_code, 302)
            self.assertTrue(response.url.startswith(reverse('login')))
