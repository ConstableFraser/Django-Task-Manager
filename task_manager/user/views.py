from django.db.models import Q
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.utils.translation import gettext_lazy as _
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from .models import User
from ..task.models import Task
from .forms import UserCreateForm, UserUpdateForm
from ..customhandlepermission import CustomHandlePermissionAuthorize
from ..messages import (USER_HAVENOT_PERMISSIONS,
                        NEED_TO_SIGNIN,
                        USER_WAS_UPDATED,
                        USER_CANT_DELETE,
                        USER_WAS_CREATED,
                        USER_HAS_BEEN_DELETE
                        )


class UserDetailView(CustomHandlePermissionAuthorize,
                     SuccessMessageMixin,
                     DetailView):
    model = User
    context_object_name = 'user'
    template_name = 'user/user_detail.html'
    permission_denied_message = _(NEED_TO_SIGNIN)

    def test_func(self):
        return self.request.user.is_authenticated

    def handle_no_permission(self):
        return self.check_for_login()

    def check_for_login(self):
        return super().check_for_login()


class UsersListView(ListView):
    model = User
    context_object_name = 'users'
    template_name = 'user/index.html'

    def get_queryset(self):
        return User.objects.all().order_by('-id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["header"] = _('Users')
        return context


class UserCreateView(SuccessMessageMixin, CreateView):
    model = User
    form_class = UserCreateForm
    template_name = 'user/user_form.html'
    success_url = reverse_lazy('login')
    success_message = _(USER_WAS_CREATED)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = _("Create a user")
        context["commit_name"] = _("Register")
        context["back_referer"] = self.request.META.get('HTTP_REFERER')
        return context


class UserUpdateView(CustomHandlePermissionAuthorize,
                     SuccessMessageMixin,
                     UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = 'user/user_form.html'
    success_url = reverse_lazy('users')
    permission_denied_message = _(NEED_TO_SIGNIN)
    success_message = _(USER_WAS_UPDATED)
    permission_denied_message = _(USER_HAVENOT_PERMISSIONS)

    def test_func(self):
        return self.request.user == self.get_object()

    def handle_no_permission(self):
        return self.check_for_authorize()

    def check_for_authorize(self):
        return super().check_for_authorize(self)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["header"] = _("Update a user")
        context["commit_name"] = _("Update")
        context["back_referer"] = self.request.META.get('HTTP_REFERER')
        return context


class UserDeleteView(CustomHandlePermissionAuthorize,
                     DeleteView):
    model = User
    template_name = 'confirm_delete.html'
    permission_denied_message = _(NEED_TO_SIGNIN)
    success_message = _(USER_HAS_BEEN_DELETE)
    success_url = reverse_lazy('users')
    permission_denied_message = _(USER_HAVENOT_PERMISSIONS)

    def test_func(self):
        return self.request.user == self.get_object()

    def handle_no_permission(self):
        return self.check_for_authorize()

    def check_for_authorize(self):
        return super().check_for_authorize(self)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["header"] = _("Delete a user")
        context["back_referer"] = self.request.META.get('HTTP_REFERER')
        return context

    def post(self, request, *args, **kwargs):
        user = self.get_object()
        tasks = Task.objects.filter(Q(executor=user) | Q(author=user))
        if tasks:
            messages.error(self.request, _(USER_CANT_DELETE))
            return HttpResponseRedirect(reverse('users'))
        else:
            messages.success(self.request, self.success_message)
            return self.delete(request, *args, **kwargs)
