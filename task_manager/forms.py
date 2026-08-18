from django import forms
from django.contrib.auth.forms import AuthenticationForm

INPUT_CLASSES = (
    'w-full rounded-md border border-gray-300 px-3 py-2 text-gray-900 '
    'focus:border-blue-500 focus:outline-none focus:ring-1 '
    'focus:ring-blue-500'
)

CHECKBOX_CLASSES = 'h-4 w-4 rounded border-gray-300 text-blue-600'


class StyledFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs['class'] = CHECKBOX_CLASSES
            else:
                field.widget.attrs['class'] = INPUT_CLASSES


class StyledFilterForm(StyledFormMixin, forms.Form):
    pass


class LoginForm(StyledFormMixin, AuthenticationForm):
    pass
