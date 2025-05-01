"""Tests for label functionality in task manager app."""
from django.urls import reverse
from task_manager.labels.models import Label
from task_manager.tasks.models import Task
from task_manager.statuses.models import Status
from .test_base import BaseTestCase, CRUDTestMixin


class LabelTestCase(BaseTestCase, CRUDTestMixin):
    """Class for Label test cases."""

    def setUp(self):
        """Setup for label tests."""
        super().setUp()
        self.status = Status.objects.create(name='Test Status')
        self.label = Label.objects.create(name='Test Label')

    model_class = Label
    base_url_name = 'label'
    create_data = {'name': 'New Test Label'}
    update_data = {'name': 'Updated Label'}

    def test_label_create_duplicate(self):
        """Test duplicate label name is not created."""
        self.login_user()
        response = self.client.post(
            reverse('label_create'),
            {'name': 'Test Label'},
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Label.objects.filter(name='Test Label').count(), 1)

    def test_label_delete_protected(self):
        """Test label in use cannot be deleted."""
        self.login_user()

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
