"""forms.py module for the task manager app."""
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


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
            raise forms.ValidationError("Password must be at least 3 characters long")
        return password1


class UserUpdateForm(forms.ModelForm):
    """Class representing UserUpdateForm logic."""
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput,
        help_text='Password must be at least 3 characters long',
        required=False
    )
    password2 = forms.CharField(
        label='Confirm password',
        widget=forms.PasswordInput,
        help_text='Please enter the same password again.',
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
                raise forms.ValidationError("Passwords do not match")
            if password1 and len(password1) < 3:
                raise forms.ValidationError("Password must be at least 3 characters long")
        return cleaned_data

    def save(self, commit=True):
        """Handles the save view logic."""
        user = super().save(commit=False)
        if self.cleaned_data.get('password1'):
            user.set_password(self.cleaned_data.get('password1'))
        if commit:
            user.save()
        return user
