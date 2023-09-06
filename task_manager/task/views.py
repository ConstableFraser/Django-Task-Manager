from django.urls import reverse_lazy
from django_filters.views import FilterView
from django.views.generic.detail import DetailView
from django.utils.translation import gettext_lazy as _
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from .models import Task
from .forms import TaskForm
from .filter import TasksFilter
from ..mixins import TaskModifyMixin, NotifyLoginRequiredMixin
from ..messages import (TASK_CREATED,
                        TASK_UPDATED,
                        TASK_DELETED,
                        NEED_TO_SIGNIN
                        )


class TaskListView(NotifyLoginRequiredMixin, FilterView):
    model = Task
    filterset_class = TasksFilter
    template_name = 'task/index.html'
    extra_content = {'header': _("Tasks")}
    permission_denied_message = _(NEED_TO_SIGNIN)


class TaskCreateView(NotifyLoginRequiredMixin,
                     SuccessMessageMixin,
                     CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'task/task_form.html'
    success_url = reverse_lazy('tasks')
    success_message = _(TASK_CREATED)
    permission_denied_message = _(NEED_TO_SIGNIN)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["header"] = _("Create task")
        context["commit_name"] = _("Create")
        context["back_referer"] = self.request.META.get('HTTP_REFERER')
        return context

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class TaskUpdateView(NotifyLoginRequiredMixin,
                     SuccessMessageMixin,
                     UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'task/task_form.html'
    success_url = reverse_lazy('tasks')
    success_message = _(TASK_UPDATED)
    permission_denied_message = _(NEED_TO_SIGNIN)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["header"] = _("Update task")
        context["commit_name"] = _("Update")
        context["back_referer"] = self.request.META.get('HTTP_REFERER')
        return context


class TaskDeleteView(TaskModifyMixin,
                     SuccessMessageMixin,
                     DeleteView):
    model = Task
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('tasks')
    success_message = _(TASK_DELETED)
    permission_denied_message = _(NEED_TO_SIGNIN)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["header"] = _("Delete task")
        context["back_referer"] = self.request.META.get('HTTP_REFERER')
        return context

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.get_context_data(object=self.object)
        return self.render_to_response(self.get_context_data())


class TaskReadView(NotifyLoginRequiredMixin, DetailView):
    model = Task
    template_name = 'task/task_card.html'
    success_url = reverse_lazy('tasks')
    permission_denied_message = _(NEED_TO_SIGNIN)
    extra_content = {'header': _("View task")}
