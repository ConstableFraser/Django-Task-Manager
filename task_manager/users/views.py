from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.utils.translation import gettext_lazy as _
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from .models import User
from .forms import UserCreateForm, UserUpdateForm
from ..mixins import (UserCanModifyMixin,
                      HandlePermissionMixin)

from ..messages import (NEED_TO_SIGNIN,
                        USER_WAS_UPDATED,
                        USER_CANT_DELETE,
                        USER_WAS_CREATED,
                        USER_HAS_BEEN_DELETE)


class UserDetailView(HandlePermissionMixin,
                     SuccessMessageMixin,
                     DetailView):
    model = User
    context_object_name = 'user'
    template_name = 'user/user_detail.html'
    required_login_message = _(NEED_TO_SIGNIN)


class UsersListView(ListView):
    model = User
    context_object_name = 'users'
    template_name = 'user/index.html'
    ordering = ['-id']
    extra_context = {'header': _('Users')}


class UserCreateView(SuccessMessageMixin, CreateView):
    model = User
    form_class = UserCreateForm
    template_name = 'user/user_form.html'
    success_url = reverse_lazy('login')
    success_message = _(USER_WAS_CREATED)
    extra_context = {'header': _("Create a user"),
                     'commit_name': _("Register")}


class UserUpdateView(UserCanModifyMixin,
                     SuccessMessageMixin,
                     UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = 'user/user_form.html'
    success_url = reverse_lazy('users')
    success_message = _(USER_WAS_UPDATED)
    extra_context = {'header': _("Update a user"),
                     'commit_name': _("Update")}


class UserDeleteView(UserCanModifyMixin,
                     DeleteView):
    model = User
    template_name = 'confirm_delete.html'
    success_message = _(USER_HAS_BEEN_DELETE)
    success_url = reverse_lazy('users')
    extra_context = {'header': _("Delete a user")}

    def post(self, request, *args, **kwargs):
        user = self.get_object()
        tasks_author = user.taskTOauthor.exists()
        tasks_executor = user.taskTOdoer.exists()
        if tasks_author or tasks_executor:
            messages.error(self.request, _(USER_CANT_DELETE))
            return redirect(reverse('users'), code=302)
        else:
            messages.success(self.request, self.success_message)
            return self.delete(request, *args, **kwargs)
