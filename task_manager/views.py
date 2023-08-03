from django.views import View
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout


class UserSignIn(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'user/user_signin.html')

    def post(self, request, *args, **kwargs):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, 'You are signed in')
            return HttpResponseRedirect("/")
        else:
            messages.error(request, 'Please enter correct username or password')
            return render(request, 'user/user_signin.html')


def logout_view(request):
    logout(request)
    messages.info(request, 'You are sign out')
    return redirect('/')
