from django.views import View
from django.urls import reverse
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import authenticate, login, logout

from .strings import (USER_SIGNIN,
                      USER_ERROR_PWD_USRNM,
                      USER_SIGNOUT,
                      )


class UserSignIn(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'user/user_signin.html')

    def post(self, request, *args, **kwargs):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user:
            login(request, user)
            messages.success(request, _(USER_SIGNIN))
            return HttpResponseRedirect(reverse("home"))
        else:
            messages.error(request, _(USER_ERROR_PWD_USRNM))
            return render(request, 'user/user_signin.html')


class LogoutView(View):
    def get(self, request):
        logout(request)
        messages.info(request, _(USER_SIGNOUT))
        return redirect('home')
