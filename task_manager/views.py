import os
from django.views import View
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

        if user is not None:
            login(request, user)
            from pathlib import Path
            BASE_DIR = Path(__file__).resolve().parent.parent
            dirs = os.listdir(BASE_DIR)
            # messages.success(request, _(USER_SIGNIN))
            messages.success(request, str(dirs))
            return HttpResponseRedirect("/")
        else:
            messages.error(request, _(USER_ERROR_PWD_USRNM))
            return render(request, 'user/user_signin.html')


def logout_view(request):
    logout(request)
    messages.info(request, _(USER_SIGNOUT))
    return redirect('/')
