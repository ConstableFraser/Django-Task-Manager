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
from ..mixins import NotifyLoginRequiredMixin
from ..messages import (STATUS_CREATED,
                        STATUS_UPDATED,
                        STATUS_DELETED,
                        STATUS_ISNOTDELETE,
                        NEED_TO_SIGNIN
                        )


class StatusListView(NotifyLoginRequiredMixin, ListView):
    redirect_field_name = ""
    raise_exception = True
    model = Status
    context_object_name = 'statuses'
    template_name = 'status/index.html'
    queryset = Status.objects.all().order_by('-id')
    extra_content = {'header': _('Statuses')}


class StatusCreateView(NotifyLoginRequiredMixin,
                       SuccessMessageMixin,
                       CreateView):
    model = Status
    form_class = StatusForm
    template_name = 'status/status_form.html'
    success_url = reverse_lazy('statuses')
    success_message = _(STATUS_CREATED)
    permission_denied_message = _(NEED_TO_SIGNIN)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["header"] = _("Create status")
        context["commit_name"] = _("Create")
        context["back_referer"] = self.request.META.get('HTTP_REFERER')
        return context


class StatusUpdateView(NotifyLoginRequiredMixin,
                       SuccessMessageMixin,
                       UpdateView):
    model = Status
    form_class = StatusForm
    template_name = 'status/status_form.html'
    success_url = reverse_lazy('statuses')
    success_message = _(STATUS_UPDATED)
    permission_denied_message = _(NEED_TO_SIGNIN)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["header"] = _("Update status")
        context["commit_name"] = _("Update")
        context["back_referer"] = self.request.META.get('HTTP_REFERER')
        return context


class StatusDeleteView(NotifyLoginRequiredMixin,
                       DeleteView):
    model = Status
    template_name = 'confirm_delete.html'
    success_message = _(STATUS_DELETED)
    success_url = reverse_lazy('statuses')
    permission_denied_message = _(NEED_TO_SIGNIN)

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
