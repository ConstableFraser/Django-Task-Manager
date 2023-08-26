from django.views import View
from django.db.models import Q
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.shortcuts import render, redirect
from django.views.generic.detail import DetailView
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from .models import User
from .forms import UserForm
from ..task.models import Task
from ..strings import (NEED_TO_SIGNIN_STR,
                       USER_WAS_UPDATED,
                       USER_HVNT_PRMSSNS,
                       USER_CANT_DELETE,
                       USER_HAS_BEEN_DELETE,
                       USER_WAS_CREATED,
                       )


class AccessControl():
    @classmethod
    def control_permissions(self, inst):
        if inst.request.user != inst.get_object():
            messages.error(inst.request, _(USER_HVNT_PRMSSNS))
            return HttpResponseRedirect(reverse('users'))
        inst.object = inst.get_object()
        inst.get_context_data(inst=inst.object)
        return inst.render_to_response(inst.get_context_data())


class UserDetailView(LoginRequiredMixin, SuccessMessageMixin, DetailView):
    model = User
    context_object_name = 'user'
    template_name = 'user/user_detail.html'
    permission_denied_message = _(NEED_TO_SIGNIN_STR)

    def handle_no_permission(self):
        messages.error(self.request, self.permission_denied_message)
        return redirect(reverse('login'), code=302)


class UsersListView(View):

    def get(self, request, *args, **kwargs):
        users = User.objects.only('id', 'username',
                                  'first_name',
                                  'last_name',
                                  'date_joined'
                                  ).order_by('-id')
        return render(request, 'user/index.html',
                      context={'users': users, 'header': _('Users')}
                      )


class UserCreateView(SuccessMessageMixin, CreateView):
    model = User
    form_class = UserForm
    template_name = 'user/user_form.html'
    success_url = reverse_lazy('login')
    success_message = _(USER_WAS_CREATED)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = _("Create a user")
        context["commit_name"] = _("Register")
        context["back_referer"] = self.request.META.get('HTTP_REFERER')
        return context


class UserUpdateView(LoginRequiredMixin,
                     SuccessMessageMixin,
                     AccessControl,
                     UpdateView):
    model = User
    form_class = UserForm
    template_name = 'user/user_form.html'
    success_url = reverse_lazy('users')
    permission_denied_message = _(NEED_TO_SIGNIN_STR)
    success_message = _(USER_WAS_UPDATED)

    def handle_no_permission(self):
        messages.error(self.request, self.permission_denied_message)
        return redirect(reverse('login'), code=302)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["header"] = _("Update a user")
        context["commit_name"] = _("Update")
        context["back_referer"] = self.request.META.get('HTTP_REFERER')
        return context

    def get(self, request, *args, **kwargs):
        return self.control_permissions(self)


class UserDeleteView(LoginRequiredMixin, AccessControl, DeleteView):
    model = User
    template_name = 'confirm_delete.html'
    permission_denied_message = _(NEED_TO_SIGNIN_STR)
    success_message = _(USER_HAS_BEEN_DELETE)
    success_url = reverse_lazy('users')

    def handle_no_permission(self):
        messages.error(self.request, self.permission_denied_message)
        return redirect(reverse('login'), code=302)

    def get(self, request, *args, **kwargs):
        return self.control_permissions(self)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["header"] = _("Delete a user")
        context["back_referer"] = self.request.META.get('HTTP_REFERER')
        return context

    def post(self, request, *args, **kwargs):
        user = self.get_object()
        tasks = Task.objects.filter(Q(executor=user) | Q(author=user))
        if not tasks:
            result = self.delete(request, *args, **kwargs)
            messages.success(self.request, self.success_message)
            return result
        else:
            messages.error(self.request, _(USER_CANT_DELETE))
            return HttpResponseRedirect(reverse('users'))
