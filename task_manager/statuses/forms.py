from django import forms
from .models import Status


class StatusForm(forms.ModelForm):
    class Meta:
        model = Status
        fields = ['name']
        error_messages = {
            'name': {
                'unique': 'Status with this name already exists',
                'required': 'This field is required'
            }
        }
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Name'
            })
        }
        labels = {
            'name': 'Name'
        }
