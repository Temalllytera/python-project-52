from django import forms
from django.contrib.auth.models import User

from task_manager.forms import StyledFormMixin
from task_manager.tasks.models import Task


class UserChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        full_name = f'{obj.first_name} {obj.last_name}'.strip()
        return full_name or obj.username


class TaskForm(StyledFormMixin, forms.ModelForm):
    executor = UserChoiceField(
        queryset=User.objects.all(),
        required=False,
        label='Исполнитель',
    )

    class Meta:
        model = Task
        fields = ['name', 'description', 'status', 'executor', 'labels']
        labels = {
            'name': 'Имя',
            'description': 'Описание',
            'status': 'Статус',
            'labels': 'Метки',
        }
        widgets = {
            'labels': forms.SelectMultiple(),
            'description': forms.Textarea(attrs={'rows': 4}),
        }
