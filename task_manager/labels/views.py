from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from task_manager.labels.forms import LabelForm
from task_manager.labels.models import Label
from task_manager.mixins import AuthRequiredMixin, DeleteProtectionMixin


class LabelListView(AuthRequiredMixin, ListView):
    model = Label
    template_name = 'labels/index.html'
    context_object_name = 'labels'


class LabelCreateView(AuthRequiredMixin, SuccessMessageMixin, CreateView):
    model = Label
    form_class = LabelForm
    template_name = 'form.html'
    success_url = reverse_lazy('labels_index')
    success_message = 'Метка успешно создана'
    extra_context = {
        'title': 'Создать метку',
        'button_text': 'Создать',
    }


class LabelUpdateView(AuthRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Label
    form_class = LabelForm
    template_name = 'form.html'
    success_url = reverse_lazy('labels_index')
    success_message = 'Метка успешно изменена'
    extra_context = {
        'title': 'Изменение метки',
        'button_text': 'Изменить',
    }


class LabelDeleteView(
    AuthRequiredMixin,
    DeleteProtectionMixin,
    SuccessMessageMixin,
    DeleteView,
):
    model = Label
    template_name = 'delete.html'
    success_url = reverse_lazy('labels_index')
    success_message = 'Метка успешно удалена'
    protected_message = (
        'Невозможно удалить метку, потому что она используется'
    )
    protected_url = reverse_lazy('labels_index')
    extra_context = {
        'title': 'Удаление метки',
        'button_text': 'Да, удалить',
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_name'] = self.object.name
        return context
