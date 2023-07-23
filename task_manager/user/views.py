from django.views import View
from django.shortcuts import render
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from .models import User
from .forms import UserForm
from ..strings import (USER_WAS_UPDATED,
                       )


class UsersListView(View):

    def get(self, request, *args, **kwargs):
        users = User.objects.only('id', 'username',
                                  'first_name',
                                  'last_name', 'date_joined'
                                  )
        return render(request, 'user/index.html',
                      context={'users': users}
                      )


class UserCreateView(CreateView):
    model = User
    form_class = UserForm
    template_name = 'user/user_form.html'
    success_url = '/login/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Create an user"
        context["commit_name"] = "Create"
        return context


class UserUpdateView(SuccessMessageMixin, UpdateView):
    model = User
    form_class = UserForm
    template_name = 'user/user_form.html'
    success_url = '/users/'
    success_message = USER_WAS_UPDATED

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Update an user"
        context["commit_name"] = "Update"
        return context


class UserDeleteView(DeleteView):
    model = User
    template_name = 'user/user_confirm_delete.html'
    success_url = '/users/'
