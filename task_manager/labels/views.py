from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.shortcuts import redirect
from task_manager.mixins import CustomLoginRequiredMixin
from django.utils.translation import gettext_lazy as _
from .models import Label
from .forms import LabelForm


class LabelListView(CustomLoginRequiredMixin, ListView):
    model = Label
    template_name = 'labels/labels.html'
    context_object_name = 'labels'


class LabelCreateView(
    CustomLoginRequiredMixin,
    SuccessMessageMixin,
    CreateView
):
    model = Label
    form_class = LabelForm
    template_name = 'labels/form.html'
    success_url = reverse_lazy('label_list')
    success_message = _('Label was successfully created')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _('Create Label')
        context['button_text'] = _('Create')
        return context


class LabelUpdateView(
    CustomLoginRequiredMixin,
    SuccessMessageMixin,
    UpdateView
):
    model = Label
    form_class = LabelForm
    template_name = 'labels/form.html'
    success_url = reverse_lazy('label_list')
    success_message = _('Label was successfully updated')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _('Edit Label')
        context['button_text'] = _('Update')
        return context


class LabelDeleteView(CustomLoginRequiredMixin, DeleteView):
    model = Label
    template_name = 'delete.html'
    success_url = reverse_lazy('label_list')
    success_message = _('Label was successfully deleted')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_type'] = _('Label')
        context['object_name'] = self.object.name
        context['cancel_url'] = reverse_lazy('label_list')
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        if self.object.tasks.exists():
            messages.error(request,
                           _('Cannot delete label because it is in use'))
            return redirect('label_list')
        try:
            self.object.delete()
            messages.success(request, self.success_message)
            return redirect(success_url)
        except Exception as e:
            messages.error(request, f'Error deleting label: {str(e)}')
            return redirect('label_list')
