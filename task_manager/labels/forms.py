from django import forms
from django.utils.translation import gettext_lazy as _

from .models import Label
from ..util import set_status
from ..messages import LABEL_EXIST


class LabelForm(forms.ModelForm):
    class Meta:
        model = Label
        fields = ['name']

    def clean(self):
        cleaned_data = super(LabelForm, self).clean()
        name = cleaned_data.get("name")
        if Label.objects.filter(name=name).exclude(id=self.instance.id):
            set_status(self.fields['name'], 'invalid')
            raise forms.ValidationError(_(LABEL_EXIST))

        return cleaned_data
