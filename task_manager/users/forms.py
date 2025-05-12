"""forms.py module for the task manager app."""
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _


class CustomUserCreationForm(UserCreationForm):
    """Class representing CustomUserCreationForm logic."""
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)

    class Meta:
        """Class representing Meta logic."""
        model = User
        fields = ['first_name', 'last_name', 'username']

    def clean_password1(self):
        """Handles the clean_password1 view logic."""
        password1 = self.cleaned_data.get('password1')
        if password1 and len(password1) < 3:
            raise forms.ValidationError(_('Password must be at least 3 '
                                          'characters long'))
        return password1


class UserUpdateForm(forms.ModelForm):
    """Class representing UserUpdateForm logic."""
    password1 = forms.CharField(
        label=_('Password'),
        widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': _('Password')
    }),
        help_text=_('Password must be at least 3 characters long'),
        required=False
    )
    password2 = forms.CharField(
        label=_('Confirm password'),
        widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': _('Confirm password')
    }),
        help_text=_('Please enter the same password again.'),
        required=False
    )

    class Meta:
        """Class representing Meta logic."""
        model = User
        fields = ['first_name', 'last_name', 'username']

    def clean(self):
        """Handles the clean view logic."""
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if password1 or password2:
            if password1 != password2:
                raise forms.ValidationError(_('Passwords do not match'))
            if password1 and len(password1) < 3:
                raise forms.ValidationError(_('Password must be at least 3 '
                                              'characters long'))
        return cleaned_data

    def save(self, commit=True):
        """Handles the save view logic."""
        user = super().save(commit=False)
        if self.cleaned_data.get('password1'):
            user.set_password(self.cleaned_data.get('password1'))
        if commit:
            user.save()
        return user
