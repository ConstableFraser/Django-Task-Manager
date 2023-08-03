from django.urls import path, re_path
from django.views.generic import TemplateView

from . import views


urlpatterns = [
    path('', views.StatusListView.as_view(), name='statuses'),
    path('create/',
         views.StatusCreateView.as_view(),
         name='status_create'),
    path('<int:pk>/update/',
         views.StatusUpdateView.as_view(),
         name='status_update'),
    path('<int:pk>/delete/',
         views.StatusDeleteView.as_view(),
         name='status_delete'),
    re_path(r'.*', TemplateView.as_view(template_name='404.html'), name='404'),
]
