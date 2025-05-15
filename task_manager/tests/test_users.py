"""Tests for user functionality in task manager app."""
from django.urls import reverse
from django.contrib.auth.models import User
from .test_base import BaseTestCase
from task_manager.statuses.models import Status
from task_manager.tasks.models import Task


class UserTestCase(BaseTestCase):
    """Class for User test cases."""

    def test_user_create(self):
        """Test user registration."""
        users_count_before = User.objects.count()
        user_data = {
            'first_name': 'Leia',
            'last_name': 'Organa',
            'username': 'leia',
            'password1': 'password123',
            'password2': 'password123'
        }
        response = self.client.post(
            reverse('user_create'),
            user_data,
            follow=True
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.count(), users_count_before + 1)
        self.assertTrue(User.objects.filter(username='luke').exists())
        self.assertRedirects(response, reverse('login'))

    def test_user_update(self):
        """Test updating user profile."""
        self.login_user()
        update_data = {
            'first_name': 'Anakin',
            'last_name': 'Skywalker',
            'username': 'darth_vader',
            'password1': 'newpassword123',
            'password2': 'newpassword123'
        }
        response = self.client.post(
            reverse('user_update', kwargs={'pk': self.user.pk}),
            update_data,
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, 'Anakin')
        self.assertEqual(self.user.last_name, 'Skywalker')
        self.assertRedirects(response, reverse('user_list'))
        self.client.logout()
        login_success = self.client.login(
            username='darth_vader',
            password='newpassword123'
        )
        self.assertTrue(login_success)

    def test_user_update_forbidden(self):
        """Users cannot update other users."""
        other_user = User.objects.create_user(
            username='leia',
            password='password123',
            first_name='Leia',
            last_name='Organa'
        )
        self.login_user()
        update_data = {
            'first_name': 'Padme',
            'last_name': 'Amidala',
            'username': 'leia',
            'password1': 'newpassword456',
            'password2': 'newpassword456'
        }
        response = self.client.post(
            reverse('user_update', kwargs={'pk': other_user.pk}),
            update_data,
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        other_user.refresh_from_db()
        self.assertEqual(other_user.first_name, 'Leia')
        self.assertEqual(other_user.last_name, 'Organa')

    def test_user_delete(self):
        """Test user deletion."""
        self.login_user()
        users_count_before = User.objects.count()
        response = self.client.post(
            reverse('user_delete', kwargs={'pk': self.user.pk}),
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.count(), users_count_before - 1)
        self.assertFalse(User.objects.filter(username='darth_vader').exists())
        self.assertRedirects(response, reverse('user_list'))

    def test_user_delete_forbidden(self):
        """Users cannot delete other users."""
        other_user = User.objects.create_user(
            username='leia',
            password='password123',
            first_name='Leia',
            last_name='Organa'
        )
        self.login_user()
        users_count_before = User.objects.count()
        response = self.client.post(
            reverse('user_delete', kwargs={'pk': other_user.pk}),
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.count(), users_count_before)
        self.assertTrue(User.objects.filter(username='leia').exists())

    def test_user_delete_protected(self):
        """Test cannot delete user with related objects."""
        self.login_user()
        status = Status.objects.create(name='Test Status')
        Task.objects.create(
            name='Task by User',
            description='Description',
            status=status,
            creator=self.user,
            executor=self.user
        )

        users_count_before = User.objects.count()
        response = self.client.post(
            reverse('user_delete', kwargs={'pk': self.user.pk}),
            follow=True
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.count(), users_count_before)
        self.assertTrue(User.objects.filter(username='darth_vader').exists())

    def test_user_list(self):
        """Test user list view."""
        response = self.client.get(reverse('user_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Darth')
        self.assertContains(response, 'Luke')

    def test_login_logout(self):
        """Test login and logout functionality."""
        login_data = {
            'username': 'darth_vader',
            'password': '123456'
        }
        response = self.client.post(
            reverse('login'),
            login_data,
            follow=True
        )
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            reverse('logout'),
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['user'].is_authenticated)
