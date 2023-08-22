from django.views import View
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.shortcuts import render, redirect
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from .models import Status
from .forms import StatusForm
from ..task.models import Task
from ..strings import (NEED_TO_SIGNIN_STR,
                       STATUS_CREATED_STR,
                       STATUS_UPDATED_STR,
                       STATUS_DELETED_STR,
                       STATUS_ISNTDELETE_STR,
                       )


class StatusListView(LoginRequiredMixin, View):
    redirect_field_name = ""
    raise_exception = True
    permission_denied_message = _(NEED_TO_SIGNIN_STR)

    def handle_no_permission(self):
        messages.success(self.request, self.permission_denied_message)
        return redirect(reverse('signin'), code=302)

    def get(self, request, *args, **kwargs):
        statuses = Status.objects.only('id', 'name',
                                       'created_at'
                                       ).order_by('-id')
        return render(request, 'status/index.html',
                      context={'statuses': statuses, 'header': _('Statuses')}
                      )


class StatusCreateView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = Status
    form_class = StatusForm
    template_name = 'status/status_form.html'
    success_url = reverse_lazy('statuses')
    success_message = _(STATUS_CREATED_STR)
    permission_denied_message = _(NEED_TO_SIGNIN_STR)

    def handle_no_permission(self):
        messages.success(self.request, self.permission_denied_message)
        return redirect(reverse('signin'), code=302)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["header"] = _("Create status")
        context["commit_name"] = _("Create")
        context["back_referer"] = self.request.META.get('HTTP_REFERER')
        return context


class StatusUpdateView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = Status
    form_class = StatusForm
    template_name = 'status/status_form.html'
    success_url = reverse_lazy('statuses')
    permission_denied_message = _(NEED_TO_SIGNIN_STR)
    success_message = _(STATUS_UPDATED_STR)

    def handle_no_permission(self):
        messages.error(self.request, self.permission_denied_message)
        return redirect(reverse('signin'), code=302)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["header"] = _("Update status")
        context["commit_name"] = _("Update")
        context["back_referer"] = self.request.META.get('HTTP_REFERER')
        return context


class StatusDeleteView(LoginRequiredMixin, DeleteView):
    model = Status
    template_name = 'confirm_delete.html'
    success_message = _(STATUS_DELETED_STR)
    success_url = reverse_lazy('statuses')
    permission_denied_message = _(NEED_TO_SIGNIN_STR)

    def handle_no_permission(self):
        messages.success(self.request, self.permission_denied_message)
        return redirect(reverse('signin'), code=302)

    def post(self, request, *args, **kwargs):
        tasks = Task.objects.filter(status=self.get_object())
        if not tasks:
            result = self.delete(request, *args, **kwargs)
            messages.success(self.request, self.success_message)
            return result
        else:
            messages.error(self.request, _(STATUS_ISNTDELETE_STR))
            return HttpResponseRedirect(reverse('statuses'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["header"] = _("Delete status")
        context["back_referer"] = self.request.META.get('HTTP_REFERER')
        return context
