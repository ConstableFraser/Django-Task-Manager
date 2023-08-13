from django.urls import path, re_path
from django.views.generic import TemplateView

from .import views
from .models import Task


urlpatterns = [
    path('', views.TaskListView.as_view(), name='tasks'),
    path('create/',
         views.TaskCreateView.as_view(),
         name='task_create'),
    path('<int:pk>/update/',
         views.TaskUpdateView.as_view(),
         name='task_update'),
    path('<int:pk>/delete/',
         views.TaskDeleteView.as_view(),
         name='task_delete'),
    path('<int:pk>/',
         views.TaskReadView.as_view(),
         name='task_read'),
    re_path(r'.*', TemplateView.as_view(template_name='404.html'), name='404'),
]
