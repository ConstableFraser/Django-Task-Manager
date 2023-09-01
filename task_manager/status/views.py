from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic.list import ListView
from django.utils.translation import gettext_lazy as _
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from .models import Status
from .forms import StatusForm
from ..task.models import Task
from ..customhandlepermission import CustomHandlePermissionAuthorize
from ..messages import (STATUS_CREATED,
                        STATUS_UPDATED,
                        STATUS_DELETED,
                        STATUS_ISNOTDELETE
                        )


class StatusListView(CustomHandlePermissionAuthorize, ListView):
    redirect_field_name = ""
    raise_exception = True
    model = Status
    context_object_name = 'statuses'
    template_name = 'status/index.html'

    def test_func(self):
        return self.request.user.is_authenticated

    def handle_no_permission(self):
        return self.check_for_login()

    def check_for_login(self):
        return super().check_for_login()

    def get_queryset(self):
        return Status.objects.all().order_by('-id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["header"] = _('Statuses')
        return context


class StatusCreateView(CustomHandlePermissionAuthorize,
                       SuccessMessageMixin,
                       CreateView):
    model = Status
    form_class = StatusForm
    template_name = 'status/status_form.html'
    success_url = reverse_lazy('statuses')
    success_message = _(STATUS_CREATED)

    def test_func(self):
        return self.request.user.is_authenticated

    def handle_no_permission(self):
        return self.check_for_login()

    def check_for_login(self):
        return super().check_for_login()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["header"] = _("Create status")
        context["commit_name"] = _("Create")
        context["back_referer"] = self.request.META.get('HTTP_REFERER')
        return context


class StatusUpdateView(CustomHandlePermissionAuthorize,
                       SuccessMessageMixin,
                       UpdateView):
    model = Status
    form_class = StatusForm
    template_name = 'status/status_form.html'
    success_url = reverse_lazy('statuses')
    success_message = _(STATUS_UPDATED)

    def test_func(self):
        return self.request.user.is_authenticated

    def handle_no_permission(self):
        return self.check_for_login()

    def check_for_login(self):
        return super().check_for_login()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["header"] = _("Update status")
        context["commit_name"] = _("Update")
        context["back_referer"] = self.request.META.get('HTTP_REFERER')
        return context


class StatusDeleteView(CustomHandlePermissionAuthorize,
                       DeleteView):
    model = Status
    template_name = 'confirm_delete.html'
    success_message = _(STATUS_DELETED)
    success_url = reverse_lazy('statuses')

    def test_func(self):
        return self.request.user.is_authenticated

    def handle_no_permission(self):
        return self.check_for_login()

    def check_for_login(self):
        return super().check_for_login()

    def post(self, request, *args, **kwargs):
        tasks = Task.objects.filter(status=self.get_object())
        if not tasks:
            result = self.delete(request, *args, **kwargs)
            messages.success(self.request, self.success_message)
            return result
        else:
            messages.error(self.request, _(STATUS_ISNOTDELETE))
            return HttpResponseRedirect(reverse('statuses'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["header"] = _("Delete status")
        context["back_referer"] = self.request.META.get('HTTP_REFERER')
        return context
