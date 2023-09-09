from django import forms
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import User


class UserCreateForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(UserCreateForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs.update({'required': True})
        self.fields['last_name'].widget.attrs.update({'required': True})

    class Meta:
        model = User
        fields = ['first_name',
                  'last_name',
                  'username']


class UserUpdateForm(UserChangeForm):
    password = None

    password1 = forms.CharField(label=_('Password'),
                                widget=forms.PasswordInput)
    password2 = forms.CharField(label=_('Confirm password'),
                                widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super(UserUpdateForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs.update({'required': True})
        self.fields['last_name'].widget.attrs.update({'required': True})

    class Meta:
        model = User
        fields = ['first_name',
                  'last_name',
                  'username']
