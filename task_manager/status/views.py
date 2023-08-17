from django.views import View
from django.contrib import messages
from django.urls import reverse, reverse_lazy
from django.shortcuts import render, redirect
from django.db.models.deletion import ProtectedError
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from .models import Status
from .forms import StatusForm
from ..strings import (NEED_TO_SIGNIN_STR,
                       STATUS_CREATED_STR,
                       STATUS_UPDATED_STR,
                       STATUS_DELETED_STR,
                       STATUS_ISNTDELETE_STR,
                       )


class StatusListView(LoginRequiredMixin, View):
    redirect_field_name = ""
    raise_exception = True
    permission_denied_message = NEED_TO_SIGNIN_STR

    def handle_no_permission(self):
        messages.success(self.request, self.permission_denied_message)
        return redirect(reverse('signin'), code=302)

    def get(self, request, *args, **kwargs):
        statuses = Status.objects.only('id', 'name',
                                       'created_at'
                                       ).order_by('-id')
        return render(request, 'status/index.html',
                      context={'statuses': statuses, 'header': 'Statuses'}
                      )


class StatusCreateView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = Status
    form_class = StatusForm
    template_name = 'status/status_form.html'
    success_url = reverse_lazy('statuses')
    success_message = STATUS_CREATED_STR
    permission_denied_message = NEED_TO_SIGNIN_STR

    def handle_no_permission(self):
        messages.success(self.request, self.permission_denied_message)
        return redirect(reverse('signin'), code=302)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["header"] = "Create status"
        context["commit_name"] = "Create"
        return context


class StatusUpdateView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = Status
    form_class = StatusForm
    template_name = 'status/status_form.html'
    success_url = reverse_lazy('statuses')
    permission_denied_message = NEED_TO_SIGNIN_STR
    success_message = STATUS_UPDATED_STR

    def handle_no_permission(self):
        messages.error(self.request, self.permission_denied_message)
        return redirect(reverse('signin'), code=302)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["header"] = "Update status"
        context["commit_name"] = "Update"
        return context


class StatusDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Status
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('statuses')
    success_message = STATUS_DELETED_STR
    
    permission_denied_message = NEED_TO_SIGNIN_STR

    def handle_no_permission(self):
        messages.success(self.request, self.permission_denied_message)
        return redirect(reverse('signin'), code=302)

    def post(self, request, *args, **kwargs):
        try:
            return self.delete(request, *args, **kwargs)
        except ProtectedError:
            messages.error(self.request, STATUS_ISNTDELETE_STR)
            return HttpResponseRedirect(reverse('statuses'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["header"] = "Delete status"
        context["back_referer"] = self.request.META.get('HTTP_REFERER')
        return context
