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
from ..mixins import UserModifyMixin, NotifyLoginRequiredMixin
from ..messages import (NEED_TO_SIGNIN,
                        USER_WAS_UPDATED,
                        USER_CANT_DELETE,
                        USER_WAS_CREATED,
                        USER_HAS_BEEN_DELETE
                        )


class UserDetailView(NotifyLoginRequiredMixin,
                     SuccessMessageMixin,
                     DetailView):
    model = User
    context_object_name = 'user'
    template_name = 'user/user_detail.html'
    permission_denied_message = _(NEED_TO_SIGNIN)


class UsersListView(ListView):
    model = User
    context_object_name = 'users'
    template_name = 'user/index.html'
    queryset = User.objects.all().order_by('-id')
    extra_context = {'header': _('Users')}


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


class UserUpdateView(UserModifyMixin,
                     SuccessMessageMixin,
                     UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = 'user/user_form.html'
    success_url = reverse_lazy('users')
    success_message = _(USER_WAS_UPDATED)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["header"] = _("Update a user")
        context["commit_name"] = _("Update")
        context["back_referer"] = self.request.META.get('HTTP_REFERER')
        return context


class UserDeleteView(UserModifyMixin,
                     DeleteView):
    model = User
    template_name = 'confirm_delete.html'
    permission_denied_message = _(NEED_TO_SIGNIN)
    success_message = _(USER_HAS_BEEN_DELETE)
    success_url = reverse_lazy('users')

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
