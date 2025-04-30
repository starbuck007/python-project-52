from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages


class CustomLoginRequiredMixin(LoginRequiredMixin):
    login_url = 'login'

    def handle_no_permission(self):
        messages.error(self.request,
                       'You are not authorized! Please log in')
        return super().handle_no_permission()
