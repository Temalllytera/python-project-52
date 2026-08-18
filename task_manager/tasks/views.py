from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from task_manager.mixins import AuthorDeletionMixin, AuthRequiredMixin
from task_manager.tasks.forms import TaskForm
from task_manager.tasks.models import Task


class TaskListView(AuthRequiredMixin, ListView):
    model = Task
    template_name = 'tasks/index.html'
    context_object_name = 'tasks'


class TaskDetailView(AuthRequiredMixin, DetailView):
    model = Task
    template_name = 'tasks/show.html'
    context_object_name = 'task'
    extra_context = {'title': 'Просмотр задачи'}


class TaskCreateView(AuthRequiredMixin, SuccessMessageMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'form.html'
    success_url = reverse_lazy('tasks_index')
    success_message = 'Задача успешно создана'
    extra_context = {
        'title': 'Создать задачу',
        'button_text': 'Создать',
    }

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class TaskUpdateView(AuthRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'form.html'
    success_url = reverse_lazy('tasks_index')
    success_message = 'Задача успешно изменена'
    extra_context = {
        'title': 'Изменение задачи',
        'button_text': 'Изменить',
    }


class TaskDeleteView(
    AuthRequiredMixin,
    AuthorDeletionMixin,
    SuccessMessageMixin,
    DeleteView,
):
    model = Task
    template_name = 'delete.html'
    success_url = reverse_lazy('tasks_index')
    success_message = 'Задача успешно удалена'
    author_message = 'Задачу может удалить только ее автор'
    author_url = reverse_lazy('tasks_index')
    extra_context = {
        'title': 'Удаление задачи',
        'button_text': 'Да, удалить',
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_name'] = self.object.name
        return context
