"""views.py module for the task manager app."""
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CustomUserCreationForm, UserUpdateForm
from django.contrib.auth import logout
from django.utils.translation import gettext_lazy as _, pgettext
from task_manager.mixins import (CustomLoginRequiredMixin,
                                 UserOwnershipRequiredMixin)
from django.db.models import ProtectedError


class UserListView(ListView):
    """Class representing UserListView logic."""
    model = User
    template_name = 'users/users.html'
    context_object_name = 'users'


class UserCreateView(SuccessMessageMixin, CreateView):
    """Class representing UserCreateView logic."""
    form_class = CustomUserCreationForm
    template_name = 'users/user_form.html'
    success_url = reverse_lazy('login')
    success_message = _('User was successfully registered')

    def get_context_data(self, **kwargs):
        """Add title and button text to context."""
        context = super().get_context_data(**kwargs)
        context['title'] = _('Register')
        context['button_text'] = pgettext('button', 'Register')
        return context


class UserUpdateView(SuccessMessageMixin, LoginRequiredMixin,
                     UserOwnershipRequiredMixin, UpdateView):
    """Class representing UserUpdateView logic."""
    model = User
    form_class = UserUpdateForm
    template_name = 'users/user_form.html'
    success_url = reverse_lazy('user_list')

    def get_context_data(self, **kwargs):
        """Add title and button text to context."""
        context = super().get_context_data(**kwargs)
        context['title'] = _('Edit user')
        context['button_text'] = _('Update')
        return context

    def form_valid(self, form):
        """Handle form validation."""
        messages.success(self.request, _('User was successfully changed'))
        user = form.save()
        if 'password1' in form.cleaned_data and form.cleaned_data['password1']:
            logout(self.request)
            return redirect(self.success_url)
        return super().form_valid(form)


class UserDeleteView(CustomLoginRequiredMixin, UserOwnershipRequiredMixin,
                     DeleteView):
    """Class representing UserDeleteView logic."""
    model = User
    template_name = 'users/delete.html'
    success_url = reverse_lazy('user_list')

    def get_context_data(self, **kwargs):
        """Handles the get_context_data view logic."""
        context = super().get_context_data(**kwargs)
        context['object_type'] = _('User')
        context['object_name'] = (self.object.get_full_name()
                                  or self.object.username)
        context['cancel_url'] = reverse_lazy('user_list')
        return context

    def post(self, request, *args, **kwargs):
        """Handle POST-request"""
        self.object = self.get_object()

        try:
            self.object.delete()
            messages.success(self.request,
                             _('User was successfully deleted'))
            logout(request)
            messages.info(request, _('You are logged out'))
            return redirect('user_list')
        except ProtectedError:
            messages.error(self.request,
                           _('Cannot delete a user because it is in use'))
            return redirect('user_list')
