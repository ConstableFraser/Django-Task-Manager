from django.urls import reverse
from django.contrib import messages
from django.shortcuts import redirect
from django.http import HttpResponseRedirect
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.mixins import UserPassesTestMixin

from .messages import NEED_TO_SIGNIN


class CustomHandlePermissionAuthorize(UserPassesTestMixin):
    def check_for_authorize(self, inst):
        redirect_url = inst.request.META.get('HTTP_REFERER')
        if inst.request.user.is_authenticated:
            messages.error(self.request, inst.permission_denied_message)
            return HttpResponseRedirect(redirect_url)
        messages.error(self.request, _(NEED_TO_SIGNIN))
        return redirect(reverse('login'), code=302)

    def check_for_login(self):
        messages.error(self.request, _(NEED_TO_SIGNIN))
        return redirect(reverse('login'), code=302)
