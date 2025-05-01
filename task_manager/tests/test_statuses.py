"""Tests for status functionality in task manager app."""
from django.urls import reverse
from task_manager.statuses.models import Status
from .test_base import BaseTestCase, CRUDTestMixin


class StatusTestCase(BaseTestCase, CRUDTestMixin):
    """Class for Status test cases."""

    def setUp(self):
        """Setup for status tests."""
        super().setUp()
        self.status = Status.objects.create(name='Test Status')

    model_class = Status
    base_url_name = 'status'
    create_data = {'name': 'New Test Status'}
    update_data = {'name': 'Updated Status'}

    def test_status_create_duplicate(self):
        """Test duplicate status name is not created."""
        self.login_user()
        response = self.client.post(
            reverse('status_create'),
            {'name': 'Test Status'},
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Status.objects.filter(name='Test Status').count(), 1)
