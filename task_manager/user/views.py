from django.views import View
from django.urls import reverse
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.db.models.deletion import ProtectedError
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from .models import User
from .forms import UserForm
from ..strings import (NEED_TO_SIGNIN_STR,
                       USER_WAS_UPDATED,
                       )


class UsersListView(View):

    def get(self, request, *args, **kwargs):
        users = User.objects.only('id', 'username',
                                  'first_name',
                                  'last_name', 'date_joined'
                                  ).order_by('-id')
        return render(request, 'user/index.html',
                      context={'users': users, 'header': 'Users'}
                      )


class UserCreateView(CreateView):
    model = User
    form_class = UserForm
    template_name = 'user/user_form.html'
    success_url = '/login/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Create a user"
        context["commit_name"] = "Create"
        return context


class UserUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = User
    form_class = UserForm
    template_name = 'user/user_form.html'
    success_url = '/users/'
    permission_denied_message = NEED_TO_SIGNIN_STR
    success_message = USER_WAS_UPDATED

    def handle_no_permission(self):
        messages.success(self.request, self.permission_denied_message)
        return redirect(reverse('signin'), code=302)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["header"] = "Update a user"
        context["commit_name"] = "Update"
        return context

    def get(self, request, *args, **kwargs):
        if self.request.user != self.get_object():
            messages.error(self.request, 'You do not have permissions to \
                                          change another user.')
            return HttpResponseRedirect('/users/')
        self.object = self.get_object()
        self.get_context_data(object=self.object)
        return self.render_to_response(self.get_context_data())


class UserDeleteView(LoginRequiredMixin, DeleteView):
    model = User
    template_name = 'confirm_delete.html'
    permission_denied_message = NEED_TO_SIGNIN_STR
    success_url = '/users/'

    def handle_no_permission(self):
        messages.success(self.request, self.permission_denied_message)
        return redirect(reverse('signin'), code=302)

    def get(self, request, *args, **kwargs):
        if self.request.user != self.get_object():
            messages.error(self.request, 'You do not have permissions to \
                                          change another user.')
            return HttpResponseRedirect('/users/')
        self.object = self.get_object()
        self.get_context_data(object=self.object)
        return self.render_to_response(self.get_context_data())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["header"] = "Delete a user"
        return context

    def post(self, request, *args, **kwargs):
        try:
            return self.delete(request, *args, **kwargs)
        except ProtectedError:
            messages.error(self.request, "Can't delete user because it's in use")
            return HttpResponseRedirect('/users/')
