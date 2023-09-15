from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views.generic.list import ListView
from django.utils.translation import gettext_lazy as _
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from .models import Status
from .forms import StatusForm
from ..mixins import HandlePermissionMixin
from ..messages import (STATUS_CREATED,
                        STATUS_UPDATED,
                        STATUS_DELETED,
                        STATUS_ISNOTDELETE,
                        NEED_TO_SIGNIN
                        )


class StatusListView(HandlePermissionMixin, ListView):
    model = Status
    context_object_name = 'statuses'
    ordering = ['-id']
    template_name = 'statuses/index.html'
    required_login_message = _(NEED_TO_SIGNIN)
    extra_context = {'header': _('Statuses')}


class StatusCreateView(HandlePermissionMixin,
                       SuccessMessageMixin,
                       CreateView):
    model = Status
    form_class = StatusForm
    template_name = 'form.html'
    success_url = reverse_lazy('statuses')
    success_message = _(STATUS_CREATED)
    required_login_message = _(NEED_TO_SIGNIN)
    extra_context = {'header': _("Create status"),
                     'commit_name': _("Create")}


class StatusUpdateView(HandlePermissionMixin,
                       SuccessMessageMixin,
                       UpdateView):
    model = Status
    form_class = StatusForm
    template_name = 'form.html'
    success_url = reverse_lazy('statuses')
    success_message = _(STATUS_UPDATED)
    required_login_message = _(NEED_TO_SIGNIN)
    extra_context = {'header': _("Update status"),
                     'commit_name': _("Update")}


class StatusDeleteView(HandlePermissionMixin,
                       DeleteView):
    model = Status
    template_name = 'confirm_delete.html'
    success_message = _(STATUS_DELETED)
    success_url = reverse_lazy('statuses')
    required_login_message = _(NEED_TO_SIGNIN)
    extra_context = {'header': _("Delete status")}

    def post(self, request, *args, **kwargs):
        status = self.get_object()
        tasks = status.task_set.exists()
        if not tasks:
            result = self.delete(request, *args, **kwargs)
            messages.success(self.request, self.success_message)
            return result
        else:
            messages.error(self.request, _(STATUS_ISNOTDELETE))
            return redirect(reverse('statuses'), code=302)
