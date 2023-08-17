from django.views import View
from django.contrib import messages
from django_filters.views import FilterView
from django.urls import reverse, reverse_lazy
from django.shortcuts import render, redirect
from django.views.generic.base import ContextMixin
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect, HttpResponseNotModified
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from .models import Task
from .forms import TaskForm
from .filter import TasksFilter
from ..strings import (NEED_TO_SIGNIN_STR,
                       TASK_CREATED_STR,
                       TASK_UPDATED_STR,
                       TASK_DELETED_STR,
                       )


class TaskListView(LoginRequiredMixin, FilterView):
    model = Task
    redirect_field_name = ""
    raise_exception = True
    permission_denied_message = NEED_TO_SIGNIN_STR
    filterset_class = TasksFilter
    template_name = 'task/index.html'

    def handle_no_permission(self):
        messages.error(self.request, self.permission_denied_message)
        return redirect(reverse('signin'), code=302)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["header"] = "Tasks"
        return context


class TaskCreateView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'task/task_form.html'
    success_url = reverse_lazy('tasks')
    success_message = TASK_CREATED_STR
    permission_denied_message = NEED_TO_SIGNIN_STR

    def handle_no_permission(self):
        messages.success(self.request, self.permission_denied_message)
        return redirect(reverse('signin'), code=302)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["header"] = "Create task"
        context["commit_name"] = "Create"
        return context

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class TaskUpdateView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'task/task_form.html'
    success_url = reverse_lazy('tasks')
    permission_denied_message = NEED_TO_SIGNIN_STR
    success_message = TASK_UPDATED_STR

    def handle_no_permission(self):
        messages.success(self.request, self.permission_denied_message)
        return redirect(reverse('signin'), code=302)

    def get_context_data(self, **kwargs):
        from django.conf import settings
        messages.info(self.request, settings.LOCALE_PATHS[0])
        context = super().get_context_data(**kwargs)
        context["header"] = "Update task"
        context["commit_name"] = "Update"
        return context


class TaskDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Task
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('tasks')
    success_message = TASK_DELETED_STR
    permission_denied_message = NEED_TO_SIGNIN_STR

    def handle_no_permission(self):
        messages.error(self.request, self.permission_denied_message)
        return redirect(reverse('signin'), code=302)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["header"] = "Delete task"
        context["back_referer"] = self.request.META.get('HTTP_REFERER')
        return context

    def get(self, request, *args, **kwargs):
        if self.request.user != self.get_object().author:
            messages.error(self.request, 'A task can only be deleted \
                                          by its author')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        self.object = self.get_object()
        self.get_context_data(object=self.object)
        return self.render_to_response(self.get_context_data())


class TaskReadView(LoginRequiredMixin, DetailView):
    model = Task
    template_name = 'task/task_card.html'
    success_url = reverse_lazy('tasks')
    permission_denied_message = NEED_TO_SIGNIN_STR

    def handle_no_permission(self):
        messages.error(self.request, self.permission_denied_message)
        return redirect(reverse('signin'), code=302)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["header"] = "View task"
        return context
