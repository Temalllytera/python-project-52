from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from task_manager.labels.models import Label


class LabelCRUDTestCase(TestCase):
    fixtures = ['users.json', 'labels.json']

    def setUp(self):
        self.user = User.objects.get(pk=1)
        self.label = Label.objects.get(pk=1)
        self.client.force_login(self.user)

    def test_labels_list(self):
        response = self.client.get(reverse('labels_index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'баг')
        self.assertContains(response, 'фича')

    def test_create_label(self):
        response = self.client.post(
            reverse('label_create'),
            {'name': 'рефакторинг'},
        )
        self.assertRedirects(response, reverse('labels_index'))
        self.assertTrue(Label.objects.filter(name='рефакторинг').exists())

    def test_create_label_with_existing_name(self):
        response = self.client.post(
            reverse('label_create'),
            {'name': 'баг'},
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Label.objects.filter(name='баг').count(), 1)

    def test_update_label(self):
        response = self.client.post(
            reverse('label_update', args=[self.label.pk]),
            {'name': 'критический баг'},
        )
        self.assertRedirects(response, reverse('labels_index'))
        self.label.refresh_from_db()
        self.assertEqual(self.label.name, 'критический баг')

    def test_delete_label(self):
        response = self.client.post(
            reverse('label_delete', args=[self.label.pk]),
        )
        self.assertRedirects(response, reverse('labels_index'))
        self.assertFalse(Label.objects.filter(pk=self.label.pk).exists())


class LabelAuthTestCase(TestCase):
    fixtures = ['users.json', 'labels.json']

    def setUp(self):
        self.label = Label.objects.get(pk=1)

    def test_list_requires_login(self):
        response = self.client.get(reverse('labels_index'))
        self.assertRedirects(response, reverse('login'))

    def test_create_requires_login(self):
        response = self.client.get(reverse('label_create'))
        self.assertRedirects(response, reverse('login'))

    def test_update_requires_login(self):
        response = self.client.get(
            reverse('label_update', args=[self.label.pk]),
        )
        self.assertRedirects(response, reverse('login'))

    def test_delete_requires_login(self):
        response = self.client.get(
            reverse('label_delete', args=[self.label.pk]),
        )
        self.assertRedirects(response, reverse('login'))
