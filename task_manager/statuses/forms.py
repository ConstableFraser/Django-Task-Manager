from django import forms
from django.utils.translation import gettext_lazy as _

from .models import Status
from ..messages import STATUS_EXIST


class StatusForm(forms.ModelForm):
    class Meta:
        model = Status
        fields = ['name']

    def clean(self):
        cleaned_data = super(StatusForm, self).clean()
        name = cleaned_data.get("name")
        if Status.objects.filter(name=name).exclude(id=self.instance.id):
            self.add_error("name", _(STATUS_EXIST))
            raise forms.ValidationError(_(STATUS_EXIST))

        return cleaned_data
