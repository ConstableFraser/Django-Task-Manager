import django_filters
from django import forms
from django_filters.widgets import BooleanWidget

from .models import Task
from ..label.models import Label

class TasksFilter(django_filters.FilterSet):
    self_tasks = django_filters.BooleanFilter(
        field_name = 'author',
        label = 'Only own tasks',
        widget = forms.CheckboxInput(),
        method = 'filter_self_tasks'
        )

    label = django_filters.ModelChoiceFilter(
        field_name = 'labels',
        label = 'Label',
        queryset = Label.objects.all().order_by('-name')
        )

    def filter_self_tasks(self, queryset, name, value):
        if value:
            return queryset.filter(author=self.request.user).order_by('-id')
        return queryset.order_by('-id')


    class Meta:
        model = Task
        fields = ['status', 'executor', 'label', 'self_tasks']
