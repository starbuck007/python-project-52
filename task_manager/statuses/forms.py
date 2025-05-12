from django import forms
from .models import Status
from django.utils.translation import gettext_lazy as _


class StatusForm(forms.ModelForm):
    class Meta:
        model = Status
        fields = ['name']
        error_messages = {
            'name': {
                'unique': _('Status with this name already exists'),
                'required': _('This field is required')
            }
        }
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': _('Name')
            })
        }
        labels = {
            'name': _('Name')
        }
