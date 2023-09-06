from django.utils.translation import gettext_lazy as _
from django.contrib.auth.views import LoginView, LogoutView

from .mixins import RedirectUserAuth
from .messages import (USER_SIGNIN,
                       USER_ERROR_PASSWORD_USERNAME,
                       USER_SIGNOUT,
                       )


class UserLoginView(RedirectUserAuth, LoginView):
    next_page = 'home'
    success_message = _(USER_SIGNIN)
    error_message = _(USER_ERROR_PASSWORD_USERNAME)


class UserLogoutView(RedirectUserAuth, LogoutView):
    next_page = 'home'
    success_message = _(USER_SIGNOUT)
