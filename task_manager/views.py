from django.urls import reverse
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.views import LoginView, LogoutView

from .messages import (USER_SIGNIN,
                       USER_ERROR_PASSWORD_USERNAME,
                       USER_SIGNOUT,
                       )


class UserLoginView(LoginView):
    redirect_authenticated_user = True
    template_name = 'user/user_signin.html'

    def get_success_url(self):
        messages.success(self.request, _(USER_SIGNIN))
        return reverse('home')

    def form_invalid(self, form):
        messages.error(self.request, _(USER_ERROR_PASSWORD_USERNAME))
        return self.render_to_response(self.get_context_data(form=form))


class UserLogoutView(LogoutView):

    def get_success_url(self):
        messages.info(self.request, _(USER_SIGNOUT))
        return reverse('home')
