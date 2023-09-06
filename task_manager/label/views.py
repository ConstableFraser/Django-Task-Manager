from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic.list import ListView
from django.utils.translation import gettext_lazy as _
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from .models import Label
from ..task.models import Task
from .forms import LabelForm
from ..mixins import NotifyLoginRequiredMixin
from ..messages import (LABEL_CREATED,
                        LABEL_UPDATED,
                        LABEL_DELETED,
                        LABEL_ISNTDELETE,
                        NEED_TO_SIGNIN
                        )


class LabelListView(NotifyLoginRequiredMixin, ListView):
    model = Label
    context_object_name = 'labels'
    template_name = 'label/index.html'
    permission_denied_message = _(NEED_TO_SIGNIN)
    queryset = Label.objects.all().order_by('-id')
    extra_context = {'header': _('Labels')}


class LabelCreateView(NotifyLoginRequiredMixin,
                      SuccessMessageMixin,
                      CreateView):
    model = Label
    form_class = LabelForm
    template_name = 'label/label_form.html'
    success_url = reverse_lazy('labels')
    success_message = _(LABEL_CREATED)
    permission_denied_message = _(NEED_TO_SIGNIN)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["header"] = _("Create label")
        context["commit_name"] = _("Create")
        context["back_referer"] = self.request.META.get('HTTP_REFERER')
        return context


class LabelUpdateView(NotifyLoginRequiredMixin,
                      SuccessMessageMixin,
                      UpdateView):
    model = Label
    form_class = LabelForm
    template_name = 'label/label_form.html'
    success_url = reverse_lazy('labels')
    success_message = _(LABEL_UPDATED)
    permission_denied_message = _(NEED_TO_SIGNIN)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["header"] = _("Update label")
        context["commit_name"] = _("Update")
        context["back_referer"] = self.request.META.get('HTTP_REFERER')
        return context


class LabelDeleteView(NotifyLoginRequiredMixin, DeleteView):
    model = Label
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('labels')
    success_message = _(LABEL_DELETED)
    permission_denied_message = _(NEED_TO_SIGNIN)

    def post(self, request, *args, **kwargs):
        tasks = Task.objects.filter(labels__in=[self.get_object()])
        if not tasks:
            result = self.delete(request, *args, **kwargs)
            messages.success(self.request, self.success_message)
            return result
        else:
            messages.error(self.request, _(LABEL_ISNTDELETE))
            return HttpResponseRedirect(reverse('labels'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["header"] = _("Delete label")
        context["back_referer"] = self.request.META.get('HTTP_REFERER')
        return context
