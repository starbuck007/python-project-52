"""Tests for main views in task manager app."""
from django.urls import reverse
from .test_base import BaseTestCase


class MainViewsTestCase(BaseTestCase):
    """Tests for main views in task manager app."""

    def test_index_view(self):
        """Test index view."""
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

    def test_login_view_get(self):
        """Test login view GET request."""
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')

    def test_login_view_success(self):
        """Test successful login."""
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
        self.assertTrue(response.context['user'].is_authenticated)

    def test_login_view_invalid_credentials(self):
        """Test login with invalid credentials."""
        login_data = {
            'username': 'darth_vader',
            'password': 'wrong_password'
        }
        response = self.client.post(
            reverse('login'),
            login_data,
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['user'].is_authenticated)

    def test_logout_view(self):
        """Test logout view."""
        self.login_user()
        self.assertTrue(self.client.session.get('_auth_user_id'))

        response = self.client.post(
            reverse('logout'),
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['user'].is_authenticated)
