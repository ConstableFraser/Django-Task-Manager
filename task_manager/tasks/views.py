from django.urls import reverse_lazy
from django_filters.views import FilterView
from django.views.generic.detail import DetailView
from django.utils.translation import gettext_lazy as _
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from .models import Task
from .forms import TaskForm
from .filter import TasksFilter
from ..mixins import TaskModifyMixin, HandlePermissionMixin
from ..messages import (TASK_CREATED,
                        TASK_UPDATED,
                        TASK_DELETED,
                        NEED_TO_SIGNIN
                        )


class TaskListView(HandlePermissionMixin, FilterView):
    model = Task
    filterset_class = TasksFilter
    template_name = 'tasks/index.html'
    extra_context = {'header': _('Tasks')}
    ordering = ['-id']
    required_login_message = _(NEED_TO_SIGNIN)


class TaskCreateView(HandlePermissionMixin,
                     SuccessMessageMixin,
                     CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'form.html'
    success_url = reverse_lazy('tasks')
    success_message = _(TASK_CREATED)
    required_login_message = _(NEED_TO_SIGNIN)
    extra_context = {'header': _("Create task"),
                     'commit_name': _("Create")}

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class TaskUpdateView(HandlePermissionMixin,
                     SuccessMessageMixin,
                     UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'form.html'
    success_url = reverse_lazy('tasks')
    success_message = _(TASK_UPDATED)
    required_login_message = _(NEED_TO_SIGNIN)
    extra_context = {'header': _("Update task"),
                     'commit_name': _("Update")}


class TaskDeleteView(TaskModifyMixin,
                     SuccessMessageMixin,
                     DeleteView):
    model = Task
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('tasks')
    success_message = _(TASK_DELETED)
    extra_context = {'header': _("Delete task")}


class TaskReadView(HandlePermissionMixin, DetailView):
    model = Task
    template_name = 'tasks/task_card.html'
    success_url = reverse_lazy('tasks')
    required_login_message = _(NEED_TO_SIGNIN)
    extra_content = {'header': _("View task")}
