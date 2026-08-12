from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from task_manager.users.forms import UserForm


class UserPermissionMixin:
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(
                request,
                'Вы не авторизованы! Пожалуйста, выполните вход.',
            )
            return redirect('login')
        if request.user.pk != self.get_object().pk:
            messages.error(
                request,
                'У вас нет прав для изменения другого пользователя.',
            )
            return redirect('users_index')
        return super().dispatch(request, *args, **kwargs)


class UserListView(ListView):
    model = User
    template_name = 'users/index.html'
    context_object_name = 'users'


class UserCreateView(SuccessMessageMixin, CreateView):
    model = User
    form_class = UserForm
    template_name = 'form.html'
    success_url = reverse_lazy('login')
    success_message = 'Пользователь успешно зарегистрирован'
    extra_context = {
        'title': 'Регистрация',
        'button_text': 'Зарегистрировать',
    }


class UserUpdateView(UserPermissionMixin, SuccessMessageMixin, UpdateView):
    model = User
    form_class = UserForm
    template_name = 'form.html'
    context_object_name = 'user_object'
    success_url = reverse_lazy('users_index')
    success_message = 'Пользователь успешно изменен'
    extra_context = {
        'title': 'Изменение пользователя',
        'button_text': 'Изменить',
    }


class UserDeleteView(UserPermissionMixin, SuccessMessageMixin, DeleteView):
    model = User
    template_name = 'delete.html'
    context_object_name = 'user_object'
    success_url = reverse_lazy('users_index')
    success_message = 'Пользователь успешно удален'
    extra_context = {
        'title': 'Удаление пользователя',
        'button_text': 'Да, удалить',
    }
