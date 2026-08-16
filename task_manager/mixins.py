from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import ProtectedError
from django.shortcuts import redirect


class AuthRequiredMixin(LoginRequiredMixin):
    auth_message = 'Вы не авторизованы! Пожалуйста, выполните вход.'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, self.auth_message)
            return redirect('login')
        return super().dispatch(request, *args, **kwargs)


class DeleteProtectionMixin:
    protected_message = ''
    protected_url = ''

    def post(self, request, *args, **kwargs):
        try:
            return super().post(request, *args, **kwargs)
        except ProtectedError:
            messages.error(request, self.protected_message)
            return redirect(self.protected_url)
