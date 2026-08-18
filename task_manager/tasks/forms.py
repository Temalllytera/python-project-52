from django import forms

from task_manager.forms import StyledFormMixin
from task_manager.tasks.models import Task


class TaskForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = Task
        fields = ['name', 'description', 'status', 'executor', 'labels']
        labels = {
            'name': 'Имя',
            'description': 'Описание',
            'status': 'Статус',
            'executor': 'Исполнитель',
            'labels': 'Метки',
        }
        widgets = {
            'labels': forms.SelectMultiple(),
            'description': forms.Textarea(attrs={'rows': 4}),
        }
