from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views.generic.list import ListView
from django.utils.translation import gettext_lazy as _
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from .models import Label
from .forms import LabelForm
from ..mixins import HandlePermissionMixin
from ..messages import (LABEL_CREATED,
                        LABEL_UPDATED,
                        LABEL_DELETED,
                        LABEL_ISNTDELETE,
                        NEED_TO_SIGNIN
                        )


class LabelListView(HandlePermissionMixin, ListView):
    model = Label
    context_object_name = 'labels'
    template_name = 'label/index.html'
    ordering = ['-id']
    required_login_message = _(NEED_TO_SIGNIN)
    extra_context = {'header': _('Labels')}


class LabelCreateView(HandlePermissionMixin,
                      SuccessMessageMixin,
                      CreateView):
    model = Label
    form_class = LabelForm
    template_name = 'label/label_form.html'
    success_url = reverse_lazy('labels')
    success_message = _(LABEL_CREATED)
    required_login_message = _(NEED_TO_SIGNIN)
    extra_context = {'header': _("Create label"),
                     'commit_name': _("Create")}


class LabelUpdateView(HandlePermissionMixin,
                      SuccessMessageMixin,
                      UpdateView):
    model = Label
    form_class = LabelForm
    template_name = 'label/label_form.html'
    success_url = reverse_lazy('labels')
    success_message = _(LABEL_UPDATED)
    required_login_message = _(NEED_TO_SIGNIN)
    extra_context = {'header': _("Update label"),
                     'commit_name': _("Update")}


class LabelDeleteView(HandlePermissionMixin, DeleteView):
    model = Label
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('labels')
    success_message = _(LABEL_DELETED)
    required_login_message = _(NEED_TO_SIGNIN)
    extra_context = {'header': _("Delete label")}

    def post(self, request, *args, **kwargs):
        label = self.get_object()
        tasks = label.task_set.exists()
        if not tasks:
            result = self.delete(request, *args, **kwargs)
            messages.success(self.request, self.success_message)
            return result
        else:
            messages.error(self.request, _(LABEL_ISNTDELETE))
            return redirect(reverse('labels'), code=302)
