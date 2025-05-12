from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.utils.translation import gettext_lazy as _


class CustomLoginRequiredMixin(LoginRequiredMixin):
    login_url = 'login'

    def handle_no_permission(self):
        messages.error(self.request,
                       _('You are not authorized! Please log in'))
        return super().handle_no_permission()
