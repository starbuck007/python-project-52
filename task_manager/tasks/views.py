from django.views.generic import (ListView, CreateView, UpdateView, DeleteView,
                                  DetailView)
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth.models import User
from .models import Task
from .forms import TaskForm
from task_manager.statuses.models import Status
from task_manager.labels.models import Label
from task_manager.mixins import CustomLoginRequiredMixin
from django.utils.translation import gettext_lazy as _


class TaskListView(CustomLoginRequiredMixin, ListView):
    model = Task
    template_name = 'tasks/tasks.html'
    context_object_name = 'tasks'

    def get_queryset(self):
        queryset = super().get_queryset()
        status_id = self.request.GET.get('status')
        if status_id:
            queryset = queryset.filter(status_id=status_id)
        executor_id = self.request.GET.get('executor')
        if executor_id:
            queryset = queryset.filter(executor_id=executor_id)
        label_id = self.request.GET.get('label')
        if label_id:
            queryset = queryset.filter(labels__id=label_id)
        only_my_tasks = self.request.GET.get('my_tasks')
        if only_my_tasks:
            queryset = queryset.filter(creator=self.request.user)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['statuses'] = Status.objects.all()
        context['users'] = User.objects.all()
        context['labels'] = Label.objects.all()
        return context


class TaskCreateView(CustomLoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/form.html'
    success_url = reverse_lazy('task_list')
    success_message = _('Task was successfully created')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        if 'executor' in form.fields:
            form.fields['executor'].queryset = User.objects.all()
        return form

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _('Create Task')
        context['button_text'] = _('Create')
        return context


class TaskUpdateView(CustomLoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/form.html'
    success_url = reverse_lazy('task_list')
    success_message = _('Task was successfully updated')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _('Edit Task')
        context['button_text'] = _('Update')
        return context

    def form_valid(self, form):
        return super().form_valid(form)


class TaskDeleteView(CustomLoginRequiredMixin, DeleteView):
    model = Task
    template_name = 'delete.html'
    success_url = reverse_lazy('task_list')
    permission_denied_message = _("You don't have permission to delete "
                                  "this task. Only the task creator can "
                                  "delete it.")

    # def test_func(self):
    #     task = self.get_object()
    #     return self.request.user == task.creator
    #
    # def handle_no_permission(self):
    #     messages.error(self.request, self.permission_denied_message)
    #     return redirect('task_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_type'] = _('Task')
        context['object_name'] = self.object.name
        context['cancel_url'] = reverse_lazy('task_list')
        return context

    # def post(self, request, *args, **kwargs):
    #     self.object = self.get_object()
    #
    #     if self.request.user != self.object.creator:
    #         messages.error(self.request, self.permission_denied_message)
    #         return redirect('task_list')
    #     try:
    #         self.object.delete()
    #         messages.success(request, _('Task was successfully deleted'))
    #         return redirect('task_list')
    #     except Exception as e:
    #         messages.error(request, f'Error deleting task: {str(e)}')
    #         return redirect('task_list')

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.request.user != self.object.creator:
            messages.error(self.request, self.permission_denied_message)
            return redirect('task_list')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        success_url = self.get_success_url()
        self.object.delete()
        messages.success(self.request, _('Task was successfully deleted'))
        return redirect(success_url)


class TaskDetailView(CustomLoginRequiredMixin, DetailView):
    model = Task
    template_name = 'tasks/task.html'
    context_object_name = 'task'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = TaskForm()
        context['labels_label'] = form.fields['labels'].label
        return context
