from django.urls import reverse
from django.contrib import messages
from django.shortcuts import redirect
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.views import RedirectURLMixin
from django.contrib.auth.mixins import (UserPassesTestMixin,
                                        LoginRequiredMixin,
                                        )


from .messages import (USER_HAVENOT_PERMISSIONS,
                       TASK_NON_AUTHOR,
                       NEED_TO_SIGNIN
                       )


class UserModifyMixin(UserPassesTestMixin, LoginRequiredMixin):
    def test_func(self):
        user = self.request.user
        return user.is_authenticated and user == self.get_object()

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            messages.error(self.request, _(USER_HAVENOT_PERMISSIONS))
            return redirect(reverse('users'), code=302)
        else:
            messages.error(self.request, _(NEED_TO_SIGNIN))
            return redirect(reverse('login'), code=302)


class TaskModifyMixin(UserPassesTestMixin, LoginRequiredMixin):
    def test_func(self):
        user = self.request.user
        return user.is_authenticated and user == self.get_object().author

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            messages.error(self.request, _(TASK_NON_AUTHOR))
            return redirect(reverse('tasks'), code=302)
        else:
            messages.error(self.request, _(NEED_TO_SIGNIN))
            return redirect(reverse('login'), code=302)


class NotifyLoginRequiredMixin(LoginRequiredMixin):
    def handle_no_permission(self):
        messages.error(self.request, _(NEED_TO_SIGNIN))
        return redirect(reverse('login'), code=302)


class RedirectUserAuth(RedirectURLMixin):
    def get_default_redirect_url(self):
        if self.next_page:
            messages.success(self.request, self.success_message)
            return reverse(self.next_page)
        else:
            messages.error(self.request, self.error_message)
        return reverse('/')

    def form_invalid(self, form):
        messages.error(self.request, self.error_message)
        return self.render_to_response(self.get_context_data(form=form))
