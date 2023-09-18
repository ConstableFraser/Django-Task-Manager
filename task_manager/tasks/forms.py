from django import forms
from django.utils.translation import gettext_lazy as _

from .models import Task
from .models import User
from .models import Status
from ..messages import TASK_EXIST, TASK_HELP


class TaskForm(forms.ModelForm):
    status = forms.ModelChoiceField(queryset=Status
                                    .objects
                                    .only('name')
                                    .order_by('name'),
                                    label=_('Status'))
    executor = forms.ModelChoiceField(queryset=User
                                      .objects
                                      .only('first_name', 'last_name')
                                      .order_by('first_name', 'last_name'),
                                      required=False,
                                      label=_('Executor'))

    class Meta:
        model = Task
        fields = ['name', 'description', 'status', 'executor', 'labels']

    def __init__(self, *args, **kwargs):
        super(TaskForm, self).__init__(*args, **kwargs)
        self.fields['name'].label = _('Name')
        self.fields['labels'].help_text = _(TASK_HELP)
        self.fields['labels'].label = _('Labels')
        self.fields['description'].label = _('Description')

    def clean(self):
        cleaned_data = super(TaskForm, self).clean()
        name = cleaned_data.get("name")
        if Task.objects.filter(name=name).exclude(id=self.instance.id):
            self.add_error("name", _(TASK_EXIST))
            raise forms.ValidationError(_(TASK_EXIST))

        return cleaned_data
