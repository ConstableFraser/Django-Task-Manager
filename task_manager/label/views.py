from django.views import View
from django.urls import reverse
from django.contrib import messages
from django.shortcuts import render, redirect
from django.db.models.deletion import ProtectedError
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.views.generic.edit import CreateView, UpdateView, DeleteView 

from .models import Label
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
    permission_denied_message = NEED_TO_SIGNIN_STR

    def handle_no_permission(self):
        messages.success(self.request, self.permission_denied_message)
        return redirect(reverse('signin'), code=302)

    def get(self, request, *args, **kwargs):
        labels = Label.objects.only('id', 'name',
                                       'created_at'
                                       ).order_by('-id')
        return render(request, 'label/index.html',
                      context={'labels': labels, 'header': 'Labels'}
                      )


class LabelCreateView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = Label
    form_class = LabelForm
    template_name = 'label/label_form.html'
    success_url = '/labels/'
    success_message = LABEL_CREATED_STR
    permission_denied_message = NEED_TO_SIGNIN_STR

    def handle_no_permission(self):
        messages.success(self.request, self.permission_denied_message)
        return redirect(reverse('signin'), code=302)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["header"] = "Create label"
        context["commit_name"] = "Create"
        return context


class LabelUpdateView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = Label
    form_class = LabelForm
    template_name = 'label/label_form.html'
    success_url = '/labels/'
    permission_denied_message = NEED_TO_SIGNIN_STR
    success_message = LABEL_UPDATED_STR

    def handle_no_permission(self):
        messages.error(self.request, self.permission_denied_message)
        return redirect(reverse('signin'), code=302)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["header"] = "Update label"
        context["commit_name"] = "Update"
        return context


class LabelDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Label
    template_name = 'confirm_delete.html'
    success_url = '/labels/'
    success_message = LABEL_DELETED_STR
    
    permission_denied_message = NEED_TO_SIGNIN_STR

    def handle_no_permission(self):
        messages.success(self.request, self.permission_denied_message)
        return redirect(reverse('signin'), code=302)

    def post(self, request, *args, **kwargs):
        try:
            return self.delete(request, *args, **kwargs)
        except ProtectedError:
            messages.error(self.request, LABEL_ISNTDELETE_STR)
            return HttpResponseRedirect('/labels/')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["header"] = "Delete label"
        return context