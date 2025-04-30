"""test_labels.py module for the task manager app."""
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from task_manager.labels.models import Label
from task_manager.tasks.models import Task
from task_manager.statuses.models import Status


class LabelTestCase(TestCase):
    """Class representing LabelTestCase logic."""

    def setUp(self):
        """Handles the setUp view logic."""
        self.user = User.objects.create_user(
            username='dark_lord',
            password='strongpassword123',
            first_name='Darth',
            last_name='Vader'
        )
        self.label = Label.objects.create(name='Test Label')
        self.client = Client()
        self.status = Status.objects.create(name='Test Status')

    def test_labels_list(self):
        """Handles the test_labels_list view logic."""
        self.client.login(username='dark_lord', password='strongpassword123')
        response = self.client.get(reverse('label_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'labels/labels.html')
        self.assertContains(response, 'Test Label')

    def test_label_create(self):
        """Handles the test_label_create view logic."""
        self.client.login(username='dark_lord', password='strongpassword123')
        response = self.client.post(
            reverse('label_create'),
            {'name': 'Test Label 2'}
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Label.objects.filter(name='Test Label 2').exists())

    def test_label_create_duplicate(self):
        """Handles the test_label_create_duplicate view logic."""
        self.client.login(username='dark_lord', password='strongpassword123')
        self.client.post(
            reverse('label_create'),
            {'name': 'Test Label'}
        )
        self.assertEqual(Label.objects.filter(name='Test Label').count(), 1)

    def test_label_update(self):
        """Handles the test_label_update view logic."""
        self.client.login(username='dark_lord', password='strongpassword123')
        response = self.client.post(
            reverse('label_update', kwargs={'pk': self.label.pk}),
            {'name': 'Updated Label'}
        )
        self.assertEqual(response.status_code, 302)
        self.label.refresh_from_db()
        self.assertEqual(self.label.name, 'Updated Label')

    def test_label_delete(self):
        """Handles the test_label_delete view logic."""
        self.client.login(username='dark_lord', password='strongpassword123')
        response = self.client.post(
            reverse('label_delete', kwargs={'pk': self.label.pk})
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Label.objects.filter(pk=self.label.pk).exists())

    def test_label_delete_protected(self):
        """Tests that a label cannot be deleted, it has a connection to the task."""
        self.client.login(username='dark_lord', password='strongpassword123')
        task = Task.objects.create(
            name='Task with Label',
            description='Task description',
            status=self.status,
            creator=self.user,
            executor=self.user
        )
        task.labels.add(self.label)
        response = self.client.post(
            reverse('label_delete', kwargs={'pk': self.label.pk}),
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Label.objects.filter(pk=self.label.pk).exists())

    def test_label_unauthorized_access(self):
        """Handles the test_label_unauthorized_access view logic."""
        urls = [
            reverse('label_list'),
            reverse('label_create'),
            reverse('label_update', kwargs={'pk': self.label.pk}),
            reverse('label_delete', kwargs={'pk': self.label.pk})
        ]
        for url in urls:
            response = self.client.get(url)
            self.assertEqual(response.status_code, 302)
            self.assertTrue(response.url.startswith(reverse('login')))
