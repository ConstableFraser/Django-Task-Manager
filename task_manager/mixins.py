from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.views import RedirectURLMixin
from django.contrib.auth.mixins import (UserPassesTestMixin,
                                        LoginRequiredMixin,
                                        )


from .messages import (USER_HAVENOT_PERMISSIONS,
                       TASK_NON_AUTHOR,
                       NEED_TO_SIGNIN
                       )


class HandlePermissionMixin(LoginRequiredMixin):
    redirect_url = reverse_lazy("login")

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            messages.error(self.request, self.required_permission_message)
            return redirect(self.redirect_field_name, code=302)
        else:
            messages.error(self.request, self.required_login_message)
            return redirect(self.redirect_url, code=302)


class UserCanModifyMixin(UserPassesTestMixin, HandlePermissionMixin):
    redirect_field_name = reverse_lazy("users")
    required_permission_message = _(USER_HAVENOT_PERMISSIONS)
    required_login_message = _(NEED_TO_SIGNIN)

    def test_func(self):
        user = self.request.user
        return user.is_authenticated and user == self.get_object()


class TaskModifyMixin(UserPassesTestMixin, HandlePermissionMixin):
    redirect_field_name = reverse_lazy("tasks")
    required_permission_message = _(TASK_NON_AUTHOR)
    required_login_message = _(NEED_TO_SIGNIN)

    def test_func(self):
        user = self.request.user
        return user.is_authenticated and user == self.get_object().author


class RedirectUserAuthMixin(RedirectURLMixin):
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
