from django import forms
from .models import Task


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['name', 'description', 'status', 'executor']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'executor': forms.Select(attrs={'class': 'form-control'}),
        }
        error_messages = {
            'name': {
                'unique': 'Task with this name already exists',
                'required': 'This field is required'
            }
        }
