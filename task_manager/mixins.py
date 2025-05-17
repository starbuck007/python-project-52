from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect
from django.contrib import messages
from django.utils.translation import gettext_lazy as _


class CustomLoginRequiredMixin(LoginRequiredMixin):
    login_url = 'login'

    def handle_no_permission(self):
        messages.error(self.request,
                       _('You are not authorized! Please log in'))
        return super().handle_no_permission()


class UserOwnershipRequiredMixin(UserPassesTestMixin):
    permission_denied_message = _(
        "You don't have permission to modify another user")

    def test_func(self):
        return self.request.user.pk == self.get_object().pk

    def handle_no_permission(self):
        storage = messages.get_messages(self.request)
        for _ in storage:
            pass
        messages.error(self.request, self.permission_denied_message)
        return redirect('user_list')
