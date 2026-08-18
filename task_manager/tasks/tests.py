from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from task_manager.labels.models import Label
from task_manager.statuses.models import Status
from task_manager.tasks.models import Task


class TaskCRUDTestCase(TestCase):
    fixtures = ['users.json', 'statuses.json', 'labels.json', 'tasks.json']

    def setUp(self):
        self.user = User.objects.get(pk=1)
        self.other_user = User.objects.get(pk=2)
        self.status = Status.objects.get(pk=1)
        self.label = Label.objects.get(pk=1)
        self.second_label = Label.objects.get(pk=2)
        self.own_task = Task.objects.get(pk=1)
        self.other_task = Task.objects.get(pk=2)
        self.client.force_login(self.user)

    def test_tasks_list(self):
        response = self.client.get(reverse('tasks_index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Написать тесты')
        self.assertContains(response, 'Задеплоить проект')

    def test_task_detail_shows_labels(self):
        response = self.client.get(
            reverse('task_show', args=[self.own_task.pk]),
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'баг')
        self.assertContains(response, 'фича')

    def test_create_task_with_labels(self):
        data = {
            'name': 'Новая задача',
            'description': 'Описание новой задачи',
            'status': self.status.pk,
            'executor': self.other_user.pk,
            'labels': [self.label.pk, self.second_label.pk],
        }
        response = self.client.post(reverse('task_create'), data)
        self.assertRedirects(response, reverse('tasks_index'))
        task = Task.objects.get(name='Новая задача')
        self.assertEqual(task.author, self.user)
        self.assertEqual(task.labels.count(), 2)

    def test_create_task_without_labels(self):
        data = {
            'name': 'Задача без меток',
            'description': '',
            'status': self.status.pk,
        }
        response = self.client.post(reverse('task_create'), data)
        self.assertRedirects(response, reverse('tasks_index'))
        task = Task.objects.get(name='Задача без меток')
        self.assertEqual(task.labels.count(), 0)

    def test_create_task_with_existing_name(self):
        data = {
            'name': 'Написать тесты',
            'description': 'Дубликат',
            'status': self.status.pk,
        }
        response = self.client.post(reverse('task_create'), data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Task.objects.filter(name='Написать тесты').count(), 1)

    def test_update_task_labels(self):
        data = {
            'name': 'Написать тесты',
            'description': 'Покрыть тестами CRUD задач',
            'status': self.status.pk,
            'executor': self.other_user.pk,
            'labels': [self.second_label.pk],
        }
        response = self.client.post(
            reverse('task_update', args=[self.own_task.pk]),
            data,
        )
        self.assertRedirects(response, reverse('tasks_index'))
        self.assertEqual(list(self.own_task.labels.all()), [self.second_label])

    def test_delete_own_task(self):
        response = self.client.post(
            reverse('task_delete', args=[self.own_task.pk]),
        )
        self.assertRedirects(response, reverse('tasks_index'))
        self.assertFalse(Task.objects.filter(pk=self.own_task.pk).exists())

    def test_delete_other_task_forbidden(self):
        response = self.client.post(
            reverse('task_delete', args=[self.other_task.pk]),
        )
        self.assertRedirects(response, reverse('tasks_index'))
        self.assertTrue(Task.objects.filter(pk=self.other_task.pk).exists())


class ProtectionTestCase(TestCase):
    fixtures = ['users.json', 'statuses.json', 'labels.json', 'tasks.json']

    def setUp(self):
        self.user = User.objects.get(pk=1)
        self.status = Status.objects.get(pk=1)
        self.used_label = Label.objects.get(pk=1)
        self.free_label = Label.objects.get(pk=3)
        self.client.force_login(self.user)

    def test_cannot_delete_status_in_use(self):
        response = self.client.post(
            reverse('status_delete', args=[self.status.pk]),
        )
        self.assertRedirects(response, reverse('statuses_index'))
        self.assertTrue(Status.objects.filter(pk=self.status.pk).exists())

    def test_cannot_delete_user_with_tasks(self):
        response = self.client.post(
            reverse('user_delete', args=[self.user.pk]),
        )
        self.assertRedirects(response, reverse('users_index'))
        self.assertTrue(User.objects.filter(pk=self.user.pk).exists())

    def test_cannot_delete_label_in_use(self):
        response = self.client.post(
            reverse('label_delete', args=[self.used_label.pk]),
        )
        self.assertRedirects(response, reverse('labels_index'))
        self.assertTrue(Label.objects.filter(pk=self.used_label.pk).exists())

    def test_can_delete_free_label(self):
        response = self.client.post(
            reverse('label_delete', args=[self.free_label.pk]),
        )
        self.assertRedirects(response, reverse('labels_index'))
        self.assertFalse(Label.objects.filter(pk=self.free_label.pk).exists())


class TaskAuthTestCase(TestCase):
    fixtures = ['users.json', 'statuses.json', 'labels.json', 'tasks.json']

    def setUp(self):
        self.task = Task.objects.get(pk=1)

    def test_list_requires_login(self):
        response = self.client.get(reverse('tasks_index'))
        self.assertRedirects(response, reverse('login'))

    def test_detail_requires_login(self):
        response = self.client.get(reverse('task_show', args=[self.task.pk]))
        self.assertRedirects(response, reverse('login'))

    def test_create_requires_login(self):
        response = self.client.get(reverse('task_create'))
        self.assertRedirects(response, reverse('login'))

    def test_delete_requires_login(self):
        response = self.client.get(reverse('task_delete', args=[self.task.pk]))
        self.assertRedirects(response, reverse('login'))
