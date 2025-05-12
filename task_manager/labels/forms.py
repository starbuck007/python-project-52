from django import forms
from .models import Label
from django.utils.translation import gettext_lazy as _


class LabelForm(forms.ModelForm):
    class Meta:
        model = Label
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'})
        }
        error_messages = {
            'name': {
                'unique': _('Label with this name already exists'),
                'required': _('This field is required')
            }
        }
