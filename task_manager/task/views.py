from django.urls import reverse_lazy
from django_filters.views import FilterView
from django.views.generic.detail import DetailView
from django.utils.translation import gettext_lazy as _
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from .models import Task
from .forms import TaskForm
from .filter import TasksFilter
from ..customhandlepermission import CustomHandlePermissionAuthorize
from ..messages import (TASK_CREATED,
                        TASK_UPDATED,
                        TASK_DELETED,
                        TASK_NON_AUTHOR,
                        )


class TaskListView(CustomHandlePermissionAuthorize, FilterView):
    model = Task
    redirect_field_name = ""
    raise_exception = True
    filterset_class = TasksFilter
    template_name = 'task/index.html'

    def test_func(self):
        return self.request.user.is_authenticated

    def handle_no_permission(self):
        return self.check_for_login()

    def check_for_login(self):
        return super().check_for_login()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["header"] = _("Tasks")
        return context


class TaskCreateView(CustomHandlePermissionAuthorize,
                     SuccessMessageMixin,
                     CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'task/task_form.html'
    success_url = reverse_lazy('tasks')
    success_message = _(TASK_CREATED)

    def test_func(self):
        return self.request.user.is_authenticated

    def handle_no_permission(self):
        return self.check_for_login()

    def check_for_login(self):
        return super().check_for_login()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["header"] = _("Create task")
        context["commit_name"] = _("Create")
        context["back_referer"] = self.request.META.get('HTTP_REFERER')
        return context

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class TaskUpdateView(CustomHandlePermissionAuthorize,
                     SuccessMessageMixin,
                     UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'task/task_form.html'
    success_url = reverse_lazy('tasks')
    success_message = _(TASK_UPDATED)

    def test_func(self):
        return self.request.user.is_authenticated

    def handle_no_permission(self):
        return self.check_for_login()

    def check_for_login(self):
        return super().check_for_login()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["header"] = _("Update task")
        context["commit_name"] = _("Update")
        context["back_referer"] = self.request.META.get('HTTP_REFERER')
        return context


class TaskDeleteView(CustomHandlePermissionAuthorize,
                     SuccessMessageMixin,
                     DeleteView):
    model = Task
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('tasks')
    success_message = _(TASK_DELETED)
    permission_denied_message = _(TASK_NON_AUTHOR)

    def test_func(self):
        return self.request.user == self.get_object().author

    def handle_no_permission(self):
        return self.check_for_authorize()

    def check_for_authorize(self):
        return super().check_for_authorize(self)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["header"] = _("Delete task")
        context["back_referer"] = self.request.META.get('HTTP_REFERER')
        return context

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.get_context_data(object=self.object)
        return self.render_to_response(self.get_context_data())


class TaskReadView(CustomHandlePermissionAuthorize, DetailView):
    model = Task
    template_name = 'task/task_card.html'
    success_url = reverse_lazy('tasks')

    def test_func(self):
        return self.request.user.is_authenticated

    def handle_no_permission(self):
        return self.check_for_login()

    def check_for_login(self):
        return super().check_for_login()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["header"] = _("View task")
        return context
