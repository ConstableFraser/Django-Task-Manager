from django import forms
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import UserCreationForm

from .models import User
from ..util import set_status
from ..messages import USER_ALREADY_EXIST


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
        user_exist = User.objects.filter(username=username).first()

        if user_exist and (user_exist != self.instance):
            set_status(self.fields['username'], 'invalid')
            raise forms.ValidationError(_(USER_ALREADY_EXIST))
        return username

    class Meta:
        model = User
        fields = ['first_name',
                  'last_name',
                  'username']
