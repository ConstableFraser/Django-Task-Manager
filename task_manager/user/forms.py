from django import forms
from django.contrib.auth import password_validation
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import User


class UserCreateForm(UserCreationForm):
    first_name = forms.CharField(label=_("First name"), required=True)
    last_name = forms.CharField(label=_("Last name"), required=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username']


class UserUpdateForm(UserChangeForm):
    first_name = forms.CharField(label=_("First name"), required=True)
    last_name = forms.CharField(label=_("Last name"), required=True)

    password = None
    help_text = password_validation.password_validators_help_text_html()
    password1 = forms.CharField(label=_("Password"),
                                widget=forms.PasswordInput(),
                                help_text=help_text)
    help_text = _("Enter the same password as before, for verification.")
    password2 = forms.CharField(label=_("Password confirmation"),
                                widget=forms.PasswordInput(),
                                help_text=help_text)

    class Meta(UserChangeForm.Meta):
        model = User
        fields = ['first_name',
                  'last_name',
                  'username',
                  'password1',
                  'password2'
                  ]
