from django.views import View
from django.urls import reverse
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect, HttpResponseNotModified
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from .models import Task
from .forms import TaskForm
from ..strings import (NEED_TO_SIGNIN_STR,
                       TASK_CREATED_STR,
                       TASK_UPDATED_STR,
                       TASK_DELETED_STR,
                       )


class TaskListView(LoginRequiredMixin, View):
    redirect_field_name = ""
    raise_exception = True
    permission_denied_message = NEED_TO_SIGNIN_STR

    def handle_no_permission(self):
        messages.success(self.request, self.permission_denied_message)
        return redirect(reverse('signin'), code=302)

    def get(self, request, *args, **kwargs):
        tasks = Task.objects.only('id',
                                  'name',
                                  'status__name',
                                  str('author'),
                                  str('executor'),
                                  'created_at'
                                  ).order_by('-id')
        return render(request, 'task/index.html',
                      context={'tasks': tasks}
                      )


class TaskCreateView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'task/task_form.html'
    success_url = '/tasks/'
    success_message = TASK_CREATED_STR
    permission_denied_message = NEED_TO_SIGNIN_STR

    def handle_no_permission(self):
        messages.success(self.request, self.permission_denied_message)
        return redirect(reverse('signin'), code=302)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Create task"
        context["commit_name"] = "Create"
        return context

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class TaskUpdateView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'task/task_form.html'
    success_url = '/tasks/'
    permission_denied_message = NEED_TO_SIGNIN_STR
    success_message = TASK_UPDATED_STR

    def handle_no_permission(self):
        messages.success(self.request, self.permission_denied_message)
        return redirect(reverse('signin'), code=302)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Update task"
        context["commit_name"] = "Update"
        return context


class TaskDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Task
    template_name = 'task/task_confirm_delete.html'
    success_url = '/tasks/'
    success_message = TASK_DELETED_STR
    permission_denied_message = NEED_TO_SIGNIN_STR

    def handle_no_permission(self):
        messages.error(self.request, self.permission_denied_message)
        return redirect(reverse('signin'), code=302)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Delete task"
        return context

    def get(self, request, *args, **kwargs):
        if self.request.user != self.get_object().author:
            messages.error(self.request, 'A task can only be deleted \
                                          by its author')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        self.object = self.get_object()
        self.get_context_data(object=self.object)
        return self.render_to_response(self.get_context_data())


class TaskReadView(LoginRequiredMixin, DeleteView):
    model = Task
    template_name = 'task/task_card.html'
    success_url = '/tasks/'
    permission_denied_message = NEED_TO_SIGNIN_STR

    def handle_no_permission(self):
        messages.success(self.request, self.permission_denied_message)
        return redirect(reverse('signin'), code=302)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "View task"
        return context
