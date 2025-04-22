"""test_users.py module for the task manager app."""
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User


class UserTestCase(TestCase):
    """Class representing UserTestCase logic."""
    def setUp(self):
        """Handles the setUp view logic."""
        self.user = User.objects.create_user(
            username='dark_lord',
            password='strongpassword123',
            first_name='Darth',
            last_name='Vader'
        )
        self.client = Client()

    def test_user_create(self):
        """Handles the test_user_create view logic."""
        users_count_before = User.objects.count()
        user_data = {
            'first_name': 'Luke',
            'last_name': 'Skywalker',
            'username': 'luke',
            'password1': 'password123',
            'password2': 'password123'
        }
        response = self.client.post(reverse('user_create'),
                                    user_data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.count(), users_count_before + 1)
        self.assertTrue(User.objects.filter(username='luke').exists())
        self.assertRedirects(response, reverse('login'))

    def test_user_update(self):
        """Handles the test_user_update view logic."""
        self.client.login(username='dark_lord', password='strongpassword123')
        update_data = {
            'first_name': 'Anakin',
            'last_name': 'Skywalker',
            'username': 'dark_lord',
            'password1': 'newpassword123',
            'password2': 'newpassword123'
        }
        response = self.client.post(
            reverse('user_update', kwargs={'pk': self.user.pk}),
            update_data,
            follow=True
        )
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, 'Anakin')
        self.assertEqual(self.user.last_name, 'Skywalker')
        self.assertRedirects(response, reverse('user_list'))
        self.client.logout()
        login_success = self.client.login(username='dark_lord',
                                          password='newpassword123')
        self.assertTrue(login_success)

    def test_user_update_forbidden(self):
        """Handles the test_user_update_forbidden view logic."""
        other_user = User.objects.create_user(
            username='leia',
            password='password123',
            first_name='Leia',
            last_name='Organa'
        )
        self.client.login(username='dark_lord', password='newpassword123')
        update_data = {
            'first_name': 'Padme',
            'last_name': 'Amidala',
            'username': 'leia',
            'password1': 'newpassword456',
            'password2': 'newpassword456'
        }
        self.client.post(
            reverse('user_update', kwargs={'pk': other_user.pk}),
            update_data,
            follow=True
        )
        other_user.refresh_from_db()
        self.assertEqual(other_user.first_name, 'Leia')
        self.assertEqual(other_user.last_name, 'Organa')

    def test_user_delete(self):
        """Handles the test_user_delete view logic."""
        self.client.login(username='dark_lord', password='strongpassword123')
        users_count_before = User.objects.count()
        response = self.client.post(
            reverse('user_delete', kwargs={'pk': self.user.pk}),
            follow=True
        )
        self.assertEqual(User.objects.count(), users_count_before - 1)
        self.assertFalse(User.objects.filter(username='dark_lord').exists())
        self.assertRedirects(response, reverse('home'))

    def test_user_delete_forbidden(self):
        """Handles the test_user_delete_forbidden view logic."""
        other_user = User.objects.create_user(
            username='leia',
            password='password123',
            first_name='Leia',
            last_name='Organa'
        )
        self.client.login(username='dark_lord', password='strongpassword123')
        users_count_before = User.objects.count()
        self.client.post(
            reverse('user_delete', kwargs={'pk': other_user.pk}),
            follow=True
        )
        self.assertEqual(User.objects.count(), users_count_before)
        self.assertTrue(User.objects.filter(username='leia').exists())
