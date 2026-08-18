from django import forms

from task_manager.forms import StyledFormMixin
from task_manager.statuses.models import Status


class StatusForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = Status
        fields = ['name']
        labels = {'name': 'Имя'}
