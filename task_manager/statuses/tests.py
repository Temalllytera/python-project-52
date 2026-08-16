from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from task_manager.statuses.models import Status


class StatusCRUDTestCase(TestCase):
    fixtures = ['users.json', 'statuses.json']

    def setUp(self):
        self.user = User.objects.get(pk=1)
        self.status = Status.objects.get(pk=1)
        self.client.force_login(self.user)

    def test_statuses_list(self):
        response = self.client.get(reverse('statuses_index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'новый')
        self.assertContains(response, 'в работе')

    def test_create_status(self):
        response = self.client.post(
            reverse('status_create'),
            {'name': 'на тестировании'},
        )
        self.assertRedirects(response, reverse('statuses_index'))
        self.assertTrue(Status.objects.filter(name='на тестировании').exists())

    def test_create_status_with_existing_name(self):
        response = self.client.post(
            reverse('status_create'),
            {'name': 'новый'},
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Status.objects.filter(name='новый').count(), 1)

    def test_update_status(self):
        response = self.client.post(
            reverse('status_update', args=[self.status.pk]),
            {'name': 'переименованный'},
        )
        self.assertRedirects(response, reverse('statuses_index'))
        self.status.refresh_from_db()
        self.assertEqual(self.status.name, 'переименованный')

    def test_delete_status(self):
        response = self.client.post(
            reverse('status_delete', args=[self.status.pk]),
        )
        self.assertRedirects(response, reverse('statuses_index'))
        self.assertFalse(Status.objects.filter(pk=self.status.pk).exists())


class StatusAuthTestCase(TestCase):
    fixtures = ['users.json', 'statuses.json']

    def setUp(self):
        self.status = Status.objects.get(pk=1)

    def test_list_requires_login(self):
        response = self.client.get(reverse('statuses_index'))
        self.assertRedirects(response, reverse('login'))

    def test_create_requires_login(self):
        response = self.client.get(reverse('status_create'))
        self.assertRedirects(response, reverse('login'))

    def test_update_requires_login(self):
        response = self.client.get(
            reverse('status_update', args=[self.status.pk]),
        )
        self.assertRedirects(response, reverse('login'))

    def test_delete_requires_login(self):
        response = self.client.get(
            reverse('status_delete', args=[self.status.pk]),
        )
        self.assertRedirects(response, reverse('login'))
