from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.shortcuts import redirect
from task_manager.mixins import CustomLoginRequiredMixin
from django.db.models import ProtectedError
from .models import Status
from .forms import StatusForm


class StatusListView(CustomLoginRequiredMixin, ListView):
    model = Status
    template_name = 'statuses/statuses.html'
    context_object_name = 'statuses'


class StatusCreateView(CustomLoginRequiredMixin,
                       SuccessMessageMixin, CreateView):
    model = Status
    form_class = StatusForm
    template_name = 'statuses/form.html'
    success_url = reverse_lazy('status_list')
    success_message = 'Status was successfully created'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Create Status'
        context['button_text'] = 'Create'
        return context


class StatusUpdateView(CustomLoginRequiredMixin,
                       SuccessMessageMixin, UpdateView):
    model = Status
    form_class = StatusForm
    template_name = 'statuses/form.html'
    success_url = reverse_lazy('status_list')
    success_message = 'Status was successfully updated'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edit Status'
        context['button_text'] = 'Edit'
        return context


class StatusDeleteView(CustomLoginRequiredMixin, DeleteView):
    model = Status
    template_name = 'delete.html'
    success_url = reverse_lazy('status_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_type'] = 'Status'
        context['object_name'] = self.object.name
        context['cancel_url'] = reverse_lazy('status_list')
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        try:
            self.object.delete()
            messages.success(self.request,
                             'Status was successfully deleted')
        except ProtectedError:
            messages.error(self.request,
                           'Cannot delete status because it is in use')
            return redirect('status_list')
        return redirect(success_url)


class StatusFormMixin:
    model = Status
    form_class = StatusForm
    success_url = reverse_lazy('status_list')
    login_url = 'login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title
        context['button_text'] = self.button_text
        return context
