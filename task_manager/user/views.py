from django.views import View
from django.shortcuts import render
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from .models import User
from .forms import UserForm


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


class UserUpdateView(UpdateView):
    model = User
    form_class = UserForm
    template_name = 'user/user_form.html'
    success_url = '/users/'


class UserDeleteView(DeleteView):
    model = User
    template_name = 'user/user_confirm_delete.html'
    success_url = '/users/'
