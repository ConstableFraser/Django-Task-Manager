from django import forms
from django.utils.translation import gettext_lazy as _

from .models import Status
from ..util import set_status
from ..strings import STATUS_EXIST_STR


class StatusForm(forms.ModelForm):
    class Meta:
        model = Status
        fields = ['name']

    def __init__(self, *args, **kwargs):
        super(StatusForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'autofocus': True,
                                                 'required': True})

    def clean(self):
        cleaned_data = super(StatusForm, self).clean()
        name = cleaned_data.get("name")
        if Status.objects.filter(name=name).exclude(id=self.instance.id):
            set_status(self.fields['name'], 'invalid')
            raise forms.ValidationError(_(STATUS_EXIST_STR))

        return cleaned_data
