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
from ..customhandlepermission import CustomHandlePermissionAuthorize
from ..messages import (LABEL_CREATED,
                        LABEL_UPDATED,
                        LABEL_DELETED,
                        LABEL_ISNTDELETE,
                        )


class LabelListView(CustomHandlePermissionAuthorize, ListView):
    redirect_field_name = ""
    raise_exception = True
    model = Label
    context_object_name = 'labels'
    template_name = 'label/index.html'

    def test_func(self):
        return self.request.user.is_authenticated

    def handle_no_permission(self):
        return self.check_for_login()

    def check_for_login(self):
        return super().check_for_login()

    def get_queryset(self):
        return Label.objects.all().order_by('-id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["header"] = _('Labels')
        return context


class LabelCreateView(CustomHandlePermissionAuthorize,
                      SuccessMessageMixin,
                      CreateView):
    model = Label
    form_class = LabelForm
    template_name = 'label/label_form.html'
    success_url = reverse_lazy('labels')
    success_message = _(LABEL_CREATED)

    def test_func(self):
        return self.request.user.is_authenticated

    def handle_no_permission(self):
        return self.check_for_login()

    def check_for_login(self):
        return super().check_for_login()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["header"] = _("Create label")
        context["commit_name"] = _("Create")
        context["back_referer"] = self.request.META.get('HTTP_REFERER')
        return context


class LabelUpdateView(CustomHandlePermissionAuthorize,
                      SuccessMessageMixin,
                      UpdateView):
    model = Label
    form_class = LabelForm
    template_name = 'label/label_form.html'
    success_url = reverse_lazy('labels')
    success_message = _(LABEL_UPDATED)

    def test_func(self):
        return self.request.user.is_authenticated

    def handle_no_permission(self):
        return self.check_for_login()

    def check_for_login(self):
        return super().check_for_login()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["header"] = _("Update label")
        context["commit_name"] = _("Update")
        context["back_referer"] = self.request.META.get('HTTP_REFERER')
        return context


class LabelDeleteView(CustomHandlePermissionAuthorize, DeleteView):
    model = Label
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('labels')
    success_message = _(LABEL_DELETED)

    def test_func(self):
        return self.request.user.is_authenticated

    def handle_no_permission(self):
        return self.check_for_login()

    def check_for_login(self):
        return super().check_for_login()

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
