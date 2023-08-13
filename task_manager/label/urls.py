from django.urls import path, re_path
from django.views.generic import TemplateView

from . import views


urlpatterns = [
    path('', views.LabelListView.as_view(), name='labels'),
    path('create/',
         views.LabelCreateView.as_view(),
         name='label_create'),
    path('<int:pk>/update/',
         views.LabelUpdateView.as_view(),
         name='label_update'),
    path('<int:pk>/delete/',
         views.LabelDeleteView.as_view(),
         name='label_delete'),
    re_path(r'.*', TemplateView.as_view(template_name='404.html'), name='404'),
]
