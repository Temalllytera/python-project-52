from django import forms

from task_manager.forms import StyledFormMixin
from task_manager.labels.models import Label


class LabelForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = Label
        fields = ['name']
        labels = {'name': 'Имя'}
