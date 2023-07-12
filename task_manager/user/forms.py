from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import (validate_password,
                                                     password_validators_help_text_html)

from .models import User
from .util import set_status


class UserForm(forms.ModelForm):
    password2 = forms.CharField(label="Confirm password",
                                widget=forms.PasswordInput(),
                                help_text="To confirm, please enter your password again.")

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'password']

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.fields['password'].widget = forms.PasswordInput()
        self.fields['password'].help_text = 'Your password must contain at least 3 characters.'
        self.fields['first_name'].widget.attrs.update({'autofocus': True, 'required': True})
        self.fields['last_name'].required = True

    def clean(self):
        cleaned_data = super(UserForm, self).clean()
        self.check_password(cleaned_data)
        self.check_username(cleaned_data)
        return cleaned_data

    def check_password(self, cleaned_data):
        password = cleaned_data.get("password")
        password2 = cleaned_data.get("password2")

        try:
            validate_password(password)
        except ValidationError:
            set_status(self.fields['password2'], 'invalid')
            set_status(self.fields['password'], 'invalid')
            raise forms.ValidationError(password_validators_help_text_html())

        if password != password2:
            set_status(self.fields['password2'], 'invalid')
            raise forms.ValidationError("The entered passwords do not match.")

    def check_username(self, cleaned_data):
        username = cleaned_data.get("username")

        def check_letter(ch: str) -> bool:
            return any([ch.isdigit(),
                        ch.isalpha(),
                        ch in ('@', '.', '+', '-', '_')
                        ])
        if not all([check_letter(s) for s in username]):
            set_status(self.fields['username'], 'invalid')
            raise forms.ValidationError("The username is required. 150 characters or fewer. Letters, digits and @/./+/-/_ only")

        if self.instance:
            exist_user = User.objects.exclude(username=self.instance.username
                                              ).filter(username=username)
            if exist_user:
                set_status(self.fields['username'], 'invalid')
                raise forms.ValidationError("A user with that username already exists")
        else:
            if User.objects.filter(username=username):
                set_status(self.fields['username'], 'invalid')
                raise forms.ValidationError("A user with that username already exists")
