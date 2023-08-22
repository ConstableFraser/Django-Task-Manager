import django_filters
from django import forms
from django.utils.translation import gettext_lazy as _
from django_filters import (BooleanFilter, ModelChoiceFilter)

from .models import Task
from ..label.models import Label
from ..user.models import User
from ..status.models import Status


class TasksFilter(django_filters.FilterSet):
    self_tasks = BooleanFilter(field_name='author',
                               widget=forms.CheckboxInput(),
                               method='filter_self_tasks',
                               label=_('Only own tasks')
                               )

    labels = Label.objects.all().order_by('name')
    label = ModelChoiceFilter(field_name='labels',
                              queryset=labels,
                              label=_('Labels'))

    users = User.objects.all().order_by('first_name')
    executor = ModelChoiceFilter(field_name='executor',
                                 queryset=users,
                                 label=_('Executor'))

    statuses = Status.objects.all().order_by('name')
    status = ModelChoiceFilter(field_name='status',
                               queryset=statuses,
                               label=_('Status'))

    def filter_self_tasks(self, queryset, name, value):
        if value:
            return queryset.filter(author=self.request.user).order_by('-id')
        return queryset.order_by('-id')

    class Meta:
        model = Task
        fields = ['status', 'executor', 'label', 'self_tasks']
