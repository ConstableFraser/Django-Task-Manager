from django.urls import path, re_path
from django.views.generic import TemplateView

from . import views


urlpatterns = [
    path('', views.UsersListView.as_view(), name='users'),
    path('create/',
         views.UserCreateView.as_view(),
         name='user_create'),
    path('<int:pk>/update/',
         views.UserUpdateView.as_view(),
         name='user_update'),
    path('<int:pk>/delete/',
         views.UserDeleteView.as_view(),
         name='user_delete'),
    path('<int:pk>/',
         views.UserDetailView.as_view(),
         name='user_card'),
    re_path(r'.*', TemplateView.as_view(template_name='404.html'), name='404'),
]
