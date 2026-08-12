from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class UserCRUDTestCase(TestCase):
    fixtures = ['users.json']

    def setUp(self):
        self.user = User.objects.get(pk=1)
        self.other_user = User.objects.get(pk=2)
        self.password = 'test-password-123'
        self.user.set_password(self.password)
        self.user.save()

    def test_users_list_available_for_guest(self):
        response = self.client.get(reverse('users_index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'ivan')
        self.assertContains(response, 'petr')

    def test_create_user(self):
        data = {
            'first_name': 'Мария',
            'last_name': 'Сидорова',
            'username': 'maria',
            'password1': 'new-password-456',
            'password2': 'new-password-456',
        }
        response = self.client.post(reverse('user_create'), data)
        self.assertRedirects(response, reverse('login'))
        self.assertTrue(User.objects.filter(username='maria').exists())

    def test_create_user_with_existing_username(self):
        data = {
            'first_name': 'Другой',
            'last_name': 'Иван',
            'username': 'ivan',
            'password1': 'new-password-456',
            'password2': 'new-password-456',
        }
        response = self.client.post(reverse('user_create'), data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.filter(username='ivan').count(), 1)

    def test_update_own_user(self):
        self.client.login(username=self.user.username, password=self.password)
        data = {
            'first_name': 'Иван',
            'last_name': 'Обновлённый',
            'username': 'ivan',
            'password1': 'another-password-789',
            'password2': 'another-password-789',
        }
        response = self.client.post(
            reverse('user_update', args=[self.user.pk]),
            data,
        )
        self.assertRedirects(response, reverse('users_index'))
        self.user.refresh_from_db()
        self.assertEqual(self.user.last_name, 'Обновлённый')

    def test_update_other_user_forbidden(self):
        self.client.login(username=self.user.username, password=self.password)
        response = self.client.get(
            reverse('user_update', args=[self.other_user.pk]),
        )
        self.assertRedirects(response, reverse('users_index'))

    def test_update_requires_login(self):
        response = self.client.get(
            reverse('user_update', args=[self.user.pk]),
        )
        self.assertRedirects(response, reverse('login'))

    def test_delete_own_user(self):
        self.client.login(username=self.user.username, password=self.password)
        response = self.client.post(
            reverse('user_delete', args=[self.user.pk]),
        )
        self.assertRedirects(response, reverse('users_index'))
        self.assertFalse(User.objects.filter(pk=self.user.pk).exists())

    def test_delete_other_user_forbidden(self):
        self.client.login(username=self.user.username, password=self.password)
        response = self.client.post(
            reverse('user_delete', args=[self.other_user.pk]),
        )
        self.assertRedirects(response, reverse('users_index'))
        self.assertTrue(User.objects.filter(pk=self.other_user.pk).exists())


class AuthTestCase(TestCase):
    fixtures = ['users.json']

    def setUp(self):
        self.user = User.objects.get(pk=1)
        self.password = 'test-password-123'
        self.user.set_password(self.password)
        self.user.save()

    def test_login(self):
        response = self.client.post(
            reverse('login'),
            {'username': self.user.username, 'password': self.password},
        )
        self.assertRedirects(response, reverse('index'))

    def test_logout(self):
        self.client.login(username=self.user.username, password=self.password)
        response = self.client.post(reverse('logout'))
        self.assertRedirects(response, reverse('index'))
