"""Tests for task functionality in task manager app."""
from django.urls import reverse
from task_manager.tasks.models import Task
from task_manager.statuses.models import Status
from task_manager.labels.models import Label
from .test_base import BaseTestCase


class TaskTestCase(BaseTestCase):
    """Class for Task test cases."""

    def setUp(self):
        """Setup for task tests."""
        super().setUp()

        self.status1 = Status.objects.create(name='Status 1')
        self.status2 = Status.objects.create(name='Status 2')

        self.task1 = Task.objects.create(
            name='Task 1',
            description='Description 1',
            status=self.status1,
            creator=self.user,
            executor=self.user
        )

        self.task2 = Task.objects.create(
            name='Task 2',
            description='Description 2',
            status=self.status2,
            creator=self.user2,
            executor=self.user
        )

    def test_task_list(self):
        """Test task list view."""
        self.login_user()
        response = self.client.get(reverse('task_list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['tasks']), 2)

    def test_task_create(self):
        """Test creating a new task."""
        self.login_user()
        task_data = {
            'name': 'New Test Task',
            'description': 'New Test Description',
            'status': self.status1.id,
            'executor': self.user2.id,
        }
        response = self.client.post(
            reverse('task_create'),
            task_data,
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Task.objects.filter(name='New Test Task').exists())
        task = Task.objects.get(name='New Test Task')
        self.assertEqual(task.creator, self.user)
        self.assertEqual(task.executor, self.user2)
        self.assertEqual(task.description, 'New Test Description')
        self.assertEqual(task.status, self.status1)

    def test_task_create_without_executor(self):
        """Test creating a task without executor."""
        self.login_user()
        task_data = {
            'name': 'Task Without Executor',
            'description': 'Task Without Executor Description',
            'status': self.status1.id,
        }
        response = self.client.post(
            reverse('task_create'),
            task_data,
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            Task.objects.filter(name='Task Without Executor').exists())
        task = Task.objects.get(name='Task Without Executor')
        self.assertIsNone(task.executor)
        self.assertEqual(task.creator, self.user)

    def test_task_create_with_labels(self):
        """Test creating a task with labels."""
        self.login_user()

        label1 = Label.objects.create(name='Label 1')
        label2 = Label.objects.create(name='Label 2')

        task_data = {
            'name': 'Task with Labels',
            'description': 'Task with multiple labels',
            'status': self.status1.id,
            'executor': self.user2.id,
            'labels': [label1.id, label2.id]
        }

        response = self.client.post(
            reverse('task_create'),
            task_data,
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        task = Task.objects.get(name='Task with Labels')
        self.assertEqual(task.labels.count(), 2)
        self.assertTrue(task.labels.filter(name='Label 1').exists())
        self.assertTrue(task.labels.filter(name='Label 2').exists())

    def test_task_update_labels(self):
        """Test updating task labels."""
        self.login_user()

        label1 = Label.objects.create(name='Label 1')
        label2 = Label.objects.create(name='Label 2')
        label3 = Label.objects.create(name='Label 3')

        self.task1.labels.add(label1, label2)

        update_data = {
            'name': self.task1.name,
            'description': self.task1.description,
            'status': self.task1.status.id,
            'executor': self.task1.executor.id,
            'labels': [label2.id, label3.id]
        }

        response = self.client.post(
            reverse('task_update', kwargs={'pk': self.task1.pk}),
            update_data,
            follow=True
        )

        self.assertEqual(response.status_code, 200)
        self.task1.refresh_from_db()
        self.assertEqual(self.task1.labels.count(), 2)
        self.assertFalse(self.task1.labels.filter(name='Label 1').exists())
        self.assertTrue(self.task1.labels.filter(name='Label 2').exists())
        self.assertTrue(self.task1.labels.filter(name='Label 3').exists())

    def test_task_update_no_executor(self):
        """Test updating a task without executor."""
        self.login_user()
        update_data = {
            'name': 'Updated Task',
            'description': 'Updated Description',
            'status': self.status1.id,
            'executor': ''
        }
        response = self.client.post(
            reverse('task_update', kwargs={'pk': self.task1.pk}),
            update_data,
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.task1.refresh_from_db()
        self.assertIsNone(self.task1.executor)
        self.assertEqual(self.task1.name, 'Updated Task')

    def test_task_delete_by_author(self):
        """Test deleting task by its author."""
        self.login_user()
        response = self.client.post(
            reverse('task_delete', kwargs={'pk': self.task1.pk}),
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Task.objects.filter(pk=self.task1.pk).exists())

    def test_task_delete_by_not_author(self):
        """Test that non-author cannot delete task."""
        self.login_user()
        response = self.client.post(
            reverse('task_delete', kwargs={'pk': self.task2.pk}),
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Task.objects.filter(pk=self.task2.pk).exists())

    def test_task_list_with_filter(self):
        """Test task list filtering."""
        self.login_user()
        response = self.client.get(reverse('task_list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['tasks']), 2)

    def test_task_my_tasks_filter(self):
        """Test filtering tasks by current user."""
        self.login_user()

        response = self.client.get(reverse('task_list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['tasks']), 2)

        response = self.client.get(f"{reverse('task_list')}?my_tasks=1")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['tasks']), 1)
        self.assertEqual(response.context['tasks'][0].name, 'Task 1')

    def test_task_filter_by_status(self):
        """Test filtering tasks by status."""
        self.login_user()

        response = self.client.get(
            f"{reverse('task_list')}?status={self.status1.id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['tasks']), 1)
        self.assertEqual(response.context['tasks'][0].name, 'Task 1')

        response = self.client.get(
            f"{reverse('task_list')}?status={self.status2.id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['tasks']), 1)
        self.assertEqual(response.context['tasks'][0].name, 'Task 2')

    def test_task_filter_by_executor(self):
        """Test filtering tasks by executor."""
        self.login_user()

        task3 = Task.objects.create(
            name='Task 3',
            description='Description 3',
            status=self.status1,
            creator=self.user,
            executor=self.user2
        )

        response = self.client.get(
            f"{reverse('task_list')}?executor={self.user.id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['tasks']), 2)

        response = self.client.get(
            f"{reverse('task_list')}?executor={self.user2.id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['tasks']), 1)
        self.assertEqual(response.context['tasks'][0].id, task3.id)

    def test_task_filter_by_label(self):
        """Test filtering tasks by label."""
        self.login_user()

        label1 = Label.objects.create(name='Filter Label 1')
        label2 = Label.objects.create(name='Filter Label 2')

        self.task1.labels.add(label1)
        self.task2.labels.add(label2)

        response = self.client.get(f"{reverse('task_list')}?label={label1.id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['tasks']), 1)
        self.assertEqual(response.context['tasks'][0].name, 'Task 1')

        response = self.client.get(f"{reverse('task_list')}?label={label2.id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['tasks']), 1)
        self.assertEqual(response.context['tasks'][0].name, 'Task 2')

    def test_task_detail_view(self):
        """Test task detail view."""
        self.login_user()
        response = self.client.get(
            reverse('task_detail', kwargs={'pk': self.task1.pk})
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['task'], self.task1)

    def test_unauthorized_access(self):
        """Unauthorized users are redirected to login."""
        self.client.logout()

        urls = [
            reverse('task_list'),
            reverse('task_create'),
            reverse('task_update', kwargs={'pk': self.task1.pk}),
            reverse('task_delete', kwargs={'pk': self.task1.pk}),
            reverse('task_detail', kwargs={'pk': self.task1.pk})
        ]

        for url in urls:
            response = self.client.get(url, follow=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn('login', response.request['PATH_INFO'])
