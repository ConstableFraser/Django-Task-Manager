from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import password_validation as pwd_validation

from .models import User
from ..util import set_status
from ..strings import (USERNAME_REQUIRED,
                       CONFIRM_PWD,
                       PWD_NOT_MATCH,
                       USER_ALREADY_EXIST,
                       PWD_TOOLTIP,
                       )


class UserForm(forms.ModelForm):
    password1 = forms.CharField(label=_("Password"),
                                widget=forms.PasswordInput(),
                                help_text=_(PWD_TOOLTIP))
    password2 = forms.CharField(label=_("Confirm password"),
                                widget=forms.PasswordInput(),
                                help_text=_(CONFIRM_PWD))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'password1']

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].required = True

    def clean(self):
        cleaned_data = super(UserForm, self).clean()
        self.check_password(cleaned_data)
        self.check_username(cleaned_data)
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user

    def check_password(self, cleaned_data):
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        try:
            pwd_validation.validate_password(str(password1))
        except ValidationError:
            set_status(self.fields['password2'], 'invalid')
            set_status(self.fields['password1'], 'invalid')
            raise forms.ValidationError(pwd_validation.
                                        password_validators_help_text_html())

        if password1 != password2:
            set_status(self.fields['password2'], 'invalid')
            raise forms.ValidationError(_(PWD_NOT_MATCH))

    def check_username(self, cleaned_data):
        username = cleaned_data.get("username")

        def check_letter(ch: str) -> bool:
            return any([ch.isdigit(),
                        ch.isalpha(),
                        ch in ('@', '.', '+', '-', '_')
                        ])
        if not all([check_letter(s) for s in username]):
            set_status(self.fields['username'], 'invalid')
            raise forms.ValidationError(_(USERNAME_REQUIRED))

        if self.instance:
            exist_user = User.objects.exclude(username=self.instance.username
                                              ).filter(username=username)
            if exist_user:
                set_status(self.fields['username'], 'invalid')
                raise forms.ValidationError(_(USER_ALREADY_EXIST))
        else:
            if User.objects.filter(username=username):
                set_status(self.fields['username'], 'invalid')
                raise forms.ValidationError(_(USER_ALREADY_EXIST))
