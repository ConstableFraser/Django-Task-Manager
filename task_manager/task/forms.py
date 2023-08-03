from django import forms

from .models import Task
from ..util import set_status
from django.contrib import messages
from ..strings import TASK_EXIST_STR


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['name', 'description', 'status', 'executor']
        # + 'label'

    def __init__(self, *args, **kwargs):
        super(TaskForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'autofocus': True,
                                                 'required': True})
        self.fields['name'].required = True
        self.fields['status'].required = True
        self.fields['executor'].required = False

    def clean(self):
        cleaned_data = super(TaskForm, self).clean()
        name = cleaned_data.get("name")
        if Task.objects.filter(name=name).exclude(id=self.instance.id):
            set_status(self.fields['name'], 'invalid')
            raise forms.ValidationError(TASK_EXIST_STR)

        return cleaned_data
