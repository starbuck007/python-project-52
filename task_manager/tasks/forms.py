from django.contrib.auth.models import User
from django import forms
from .models import Task
from django.utils.translation import gettext_lazy as _


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['name', 'description', 'status', 'executor', 'labels']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'executor': forms.Select(attrs={'class': 'form-control',
                                            'id': 'id_executor'}),
            'labels': forms.SelectMultiple(attrs={'class': 'form-control',
                                                  'multiple': 'multiple'}),
        }
        labels = {
            'name': _('Name'),
            'description': _('Description'),
            'status': _('Status'),
            'executor': _('Executor'),
            'labels': _('Labels')
        }
        error_messages = {
            'name': {
                'unique': _('Task with this name already exists'),
                'required': _('This field is required')
            }
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['executor'].label = _('Executor')
        self.fields['executor'].required = False
        self.fields['executor'].queryset = User.objects.all()
        self.fields['executor'].label_from_instance = lambda \
            user: user.get_full_name() or user.username
        self.fields['executor'].widget.attrs.update(
            {'id': 'id_executor', 'class': 'form-control'})
        if self.instance and self.instance.pk and self.instance.executor:
            self.initial['executor'] = self.instance.executor.id
