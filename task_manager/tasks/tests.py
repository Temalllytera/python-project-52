from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from task_manager.statuses.models import Status
from task_manager.tasks.models import Task


class TaskCRUDTestCase(TestCase):
    fixtures = ['users.json', 'statuses.json', 'tasks.json']

    def setUp(self):
        self.user = User.objects.get(pk=1)
        self.other_user = User.objects.get(pk=2)
        self.status = Status.objects.get(pk=1)
        self.own_task = Task.objects.get(pk=1)
        self.other_task = Task.objects.get(pk=2)
        self.client.force_login(self.user)

    def test_tasks_list(self):
        response = self.client.get(reverse('tasks_index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Написать тесты')
        self.assertContains(response, 'Задеплоить проект')

    def test_task_detail(self):
        response = self.client.get(
            reverse('task_show', args=[self.own_task.pk]),
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Покрыть тестами CRUD задач')

    def test_create_task(self):
        data = {
            'name': 'Новая задача',
            'description': 'Описание новой задачи',
            'status': self.status.pk,
            'executor': self.other_user.pk,
        }
        response = self.client.post(reverse('task_create'), data)
        self.assertRedirects(response, reverse('tasks_index'))
        task = Task.objects.get(name='Новая задача')
        self.assertEqual(task.author, self.user)

    def test_create_task_with_existing_name(self):
        data = {
            'name': 'Написать тесты',
            'description': 'Дубликат',
            'status': self.status.pk,
        }
        response = self.client.post(reverse('task_create'), data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Task.objects.filter(name='Написать тесты').count(), 1)

    def test_update_task(self):
        data = {
            'name': 'Переименованная задача',
            'description': 'Обновлённое описание',
            'status': self.status.pk,
            'executor': self.other_user.pk,
        }
        response = self.client.post(
            reverse('task_update', args=[self.own_task.pk]),
            data,
        )
        self.assertRedirects(response, reverse('tasks_index'))
        self.own_task.refresh_from_db()
        self.assertEqual(self.own_task.name, 'Переименованная задача')

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


class TaskProtectionTestCase(TestCase):
    fixtures = ['users.json', 'statuses.json', 'tasks.json']

    def setUp(self):
        self.user = User.objects.get(pk=1)
        self.status = Status.objects.get(pk=1)
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


class TaskAuthTestCase(TestCase):
    fixtures = ['users.json', 'statuses.json', 'tasks.json']

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
