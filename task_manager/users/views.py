"""views.py module for the task manager app."""
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from .forms import CustomUserCreationForm, UserUpdateForm
from django.contrib.auth import logout


class UserListView(ListView):
    """Class representing UserListView logic."""
    model = User
    template_name = 'users/users.html'
    context_object_name = 'users'


class UserCreateView(SuccessMessageMixin, CreateView):
    """Class representing UserCreateView logic."""
    form_class = CustomUserCreationForm
    template_name = 'users/create.html'
    success_url = reverse_lazy('login')
    success_message = 'User was successfully registered'


class UserUpdateView(LoginRequiredMixin, UserPassesTestMixin,
                     SuccessMessageMixin, UpdateView):
    """Class representing UserUpdateView logic."""
    model = User
    form_class = UserUpdateForm
    template_name = 'users/update.html'
    success_url = reverse_lazy('user_list')
    success_message = 'User was successfully updated'

    def test_func(self):
        """Handles the test_func view logic."""
        return self.request.user.pk == self.get_object().pk

    def handle_no_permission(self):
        """Handles the handle_no_permission view logic."""
        messages.error(self.request,
                       "You don't have permission to change another user.")
        return redirect('user_list')


class UserDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Class representing UserDeleteView logic."""
    model = User
    template_name = 'users/delete.html'
    success_url = reverse_lazy('user_list')

    def test_func(self):
        """Handles the test_func view logic."""
        return self.request.user.pk == self.get_object().pk

    def handle_no_permission(self):
        """Handles the handle_no_permission view logic."""
        messages.error(self.request,
                       "You don't have permission to delete another user.")
        return redirect('user_list')

    def post(self, request, *args, **kwargs):
        """Handles the post view logic."""
        self.object = self.get_object()
        is_self_deletion = self.object == request.user
        self.object.delete()
        messages.success(request, 'User was successfully deleted')
        if is_self_deletion:
            logout(request)
            messages.info(request, 'You are logged out')
            return redirect('home')
        return redirect(self.success_url)
