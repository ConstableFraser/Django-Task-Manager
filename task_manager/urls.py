from django.contrib import admin
from django.views.generic import TemplateView
from django.urls import include, path, re_path

from .views import UserSignIn, LogoutView


urlpatterns = [
    path('', TemplateView.as_view(template_name='index.html'), name='home'),
    path('admin/', admin.site.urls),
    path('login/', UserSignIn.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='signout'),
    path('users/', include('task_manager.user.urls')),
    path('statuses/', include('task_manager.status.urls')),
    path('tasks/', include('task_manager.task.urls')),
    path('labels/', include('task_manager.label.urls')),
    re_path(r'.*', TemplateView.as_view(template_name='404.html'), name='404'),
]
