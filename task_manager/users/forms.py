from django import forms
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import UserCreationForm

from .models import User
from ..util import validate_username, set_status
from ..messages import USERNAME_INCORRECT


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


class UserUpdateForm(UserCreateForm):
    def clean_username(self):
        username = self.cleaned_data["username"]
        if not validate_username(username):
            set_status(self.fields['username'], 'invalid')
            raise forms.ValidationError(_(USERNAME_INCORRECT))
        return username

    class Meta:
        model = User
        fields = ['first_name',
                  'last_name',
                  'username']
