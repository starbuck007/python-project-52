"""test_tasks.py module for the task manager app."""
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from task_manager.tasks.models import Task
from task_manager.statuses.models import Status
from task_manager.labels.models import Label


class TaskTestCase(TestCase):
    """Class representing TaskTestCase logic."""
    def setUp(self):
        """Handles the setUp view logic."""
        self.user1 = User.objects.create_user(
            username='darth_vader',
            password='12345',
            first_name='Darth',
            last_name='Vader'
        )
        self.user2 = User.objects.create_user(
            username='luke',
            password='54321',
            first_name='Luke',
            last_name='Skywalker'
        )
        self.status1 = Status.objects.create(name='Status 1')
        self.status2 = Status.objects.create(name='Status 2')

        self.task1 = Task.objects.create(
            name='Task 1',
            description='Description 1',
            status=self.status1,
            creator=self.user1,
            executor=self.user1
        )
        self.task2 = Task.objects.create(
            name='Task 2',
            description='Description 2',
            status=self.status2,
            creator=self.user2,
            executor=self.user1
        )
        self.client = Client()

    def test_task_create(self):
        self.client.login(username='darth_vader', password='12345')
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
        self.assertEqual(task.creator, self.user1)
        self.assertEqual(task.executor, self.user2)
        self.assertEqual(task.description, 'New Test Description')
        self.assertEqual(task.status, self.status1)

    def test_task_create_without_executor(self):
        self.client.login(username='darth_vader', password='12345')
        task_data = {
            'name': 'Task Without Executor',
            'description': 'No executor specified',
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
        self.assertEqual(task.executor, self.user1)
        self.assertEqual(task.creator, self.user1)

    def test_task_create_with_labels(self):
        """Tests creating a task with labels."""
        self.client.login(username='darth_vader', password='12345')
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
        self.assertTrue(Task.objects.filter(name='Task with Labels').exists())
        task = Task.objects.get(name='Task with Labels')
        self.assertEqual(task.labels.count(), 2)
        self.assertTrue(task.labels.filter(name='Label 1').exists())
        self.assertTrue(task.labels.filter(name='Label 2').exists())

    def test_task_update_labels(self):
        """Tests updating task labels."""
        self.client.login(username='darth_vader', password='12345')
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
        self.client.login(username='darth_vader', password='12345')
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
        self.assertEqual(self.task1.executor, self.user1)
        self.assertEqual(self.task1.name, 'Updated Task')

    def test_task_delete_by_author(self):
        self.client.login(username='darth_vader', password='12345')
        response = self.client.post(
            reverse('task_delete', kwargs={'pk': self.task1.pk}),
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Task.objects.filter(pk=self.task1.pk).exists())

    def test_task_delete_by_not_author(self):
        self.client.login(username='darth_vader', password='12345')
        response = self.client.post(
            reverse('task_delete', kwargs={'pk': self.task2.pk}),
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Task.objects.filter(pk=self.task2.pk).exists())

    def test_task_list_with_filter(self):
        self.client.login(username='darth_vader', password='12345')
        response = self.client.get(reverse('task_list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['tasks']), 2)

    def test_task_my_tasks_filter(self):
        self.client.login(username='darth_vader', password='12345')

        response = self.client.get(reverse('task_list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['tasks']), 2)

        response = self.client.get(f"{reverse('task_list')}?my_tasks=1")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['tasks']), 1)
        self.assertEqual(response.context['tasks'][0].name, 'Task 1')

    def test_task_filter_by_label(self):
        """Tests filtering tasks by label."""
        self.client.login(username='darth_vader', password='12345')
        label1 = Label.objects.create(name='Filter Label')
        label2 = Label.objects.create(name='Other Label')
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
