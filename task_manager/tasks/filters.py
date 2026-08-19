import django_filters
from django import forms
from django.contrib.auth.models import User

from task_manager.forms import StyledFilterForm
from task_manager.labels.models import Label
from task_manager.tasks.forms import UserChoiceField
from task_manager.tasks.models import Task


class UserFilterField(django_filters.ModelChoiceFilter):
    field_class = UserChoiceField


class TaskFilter(django_filters.FilterSet):
    executor = UserFilterField(
        queryset=User.objects.all(),
        label='Исполнитель',
    )
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
        form = StyledFilterForm

    def filter_self_tasks(self, queryset, name, value):
        if value:
            return queryset.filter(author=self.request.user)
        return queryset
