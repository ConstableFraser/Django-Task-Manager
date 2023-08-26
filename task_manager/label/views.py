from django.views import View
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.shortcuts import render, redirect
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from .models import Label
from ..task.models import Task
from .forms import LabelForm
from ..strings import (NEED_TO_SIGNIN_STR,
                       LABEL_CREATED_STR,
                       LABEL_UPDATED_STR,
                       LABEL_DELETED_STR,
                       LABEL_ISNTDELETE_STR,
                       )


class LabelListView(LoginRequiredMixin, View):
    redirect_field_name = ""
    raise_exception = True
    permission_denied_message = _(NEED_TO_SIGNIN_STR)

    def handle_no_permission(self):
        messages.error(self.request, self.permission_denied_message)
        return redirect(reverse('login'), code=302)

    def get(self, request, *args, **kwargs):
        labels = Label.objects.only('id', 'name',
                                    'created_at'
                                    ).order_by('-id')
        return render(request, 'label/index.html',
                      context={'labels': labels, 'header': _('Labels')}
                      )


class LabelCreateView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = Label
    form_class = LabelForm
    template_name = 'label/label_form.html'
    success_url = reverse_lazy('labels')
    success_message = _(LABEL_CREATED_STR)
    permission_denied_message = _(NEED_TO_SIGNIN_STR)

    def handle_no_permission(self):
        messages.error(self.request, self.permission_denied_message)
        return redirect(reverse('login'), code=302)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["header"] = _("Create label")
        context["commit_name"] = _("Create")
        context["back_referer"] = self.request.META.get('HTTP_REFERER')
        return context


class LabelUpdateView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = Label
    form_class = LabelForm
    template_name = 'label/label_form.html'
    success_url = reverse_lazy('labels')
    permission_denied_message = _(NEED_TO_SIGNIN_STR)
    success_message = _(LABEL_UPDATED_STR)

    def handle_no_permission(self):
        messages.error(self.request, self.permission_denied_message)
        return redirect(reverse('login'), code=302)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["header"] = _("Update label")
        context["commit_name"] = _("Update")
        context["back_referer"] = self.request.META.get('HTTP_REFERER')
        return context


class LabelDeleteView(LoginRequiredMixin, DeleteView):
    model = Label
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('labels')
    success_message = _(LABEL_DELETED_STR)

    permission_denied_message = _(NEED_TO_SIGNIN_STR)

    def handle_no_permission(self):
        messages.error(self.request,
                       self.permission_denied_message)
        return redirect(reverse('login'), code=302)

    def post(self, request, *args, **kwargs):
        tasks = Task.objects.filter(labels__in=[self.get_object()])
        if not tasks:
            result = self.delete(request, *args, **kwargs)
            messages.success(self.request, self.success_message)
            return result
        else:
            messages.error(self.request, _(LABEL_ISNTDELETE_STR))
            return HttpResponseRedirect(reverse('labels'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["header"] = _("Delete label")
        context["back_referer"] = self.request.META.get('HTTP_REFERER')
        return context
