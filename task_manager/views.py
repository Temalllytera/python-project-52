from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import TemplateView


class IndexView(TemplateView):
    template_name = 'index.html'


class UserLoginView(SuccessMessageMixin, LoginView):
    template_name = 'form.html'
    next_page = reverse_lazy('index')
    success_message = 'Вы залогинены'
    extra_context = {
        'title': 'Вход',
        'button_text': 'Войти',
    }


class UserLogoutView(LogoutView):
    next_page = reverse_lazy('index')

    def post(self, request, *args, **kwargs):
        messages.info(request, 'Вы разлогинены')
        return super().post(request, *args, **kwargs)
