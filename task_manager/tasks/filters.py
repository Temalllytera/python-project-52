import django_filters
from django import forms

from task_manager.labels.models import Label
from task_manager.tasks.models import Task


class TaskFilter(django_filters.FilterSet):
    labels = django_filters.ModelChoiceFilter(
        queryset=Label.objects.all(),
        label='Метка',
    )
    self_tasks = django_filters.BooleanFilter(
        label='Только свои задачи',
        widget=forms.CheckboxInput,
        method='filter_self_tasks',
    )

    class Meta:
        model = Task
        fields = ['status', 'executor', 'labels']

    def filter_self_tasks(self, queryset, name, value):
        if value:
            return queryset.filter(author=self.request.user)
        return queryset
