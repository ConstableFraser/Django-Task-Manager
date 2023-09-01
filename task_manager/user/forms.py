from django import forms
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
    password = None

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username']
