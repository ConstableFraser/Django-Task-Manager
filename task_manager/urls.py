from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView

from .views import UserLoginView, UserLogoutView

urlpatterns = [
    path('', TemplateView.as_view(template_name='index.html'), name='home'),
    path('admin/', admin.site.urls),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='signout'),
    path('users/', include('task_manager.user.urls')),
    path('statuses/', include('task_manager.status.urls')),
    path('tasks/', include('task_manager.task.urls')),
    path('labels/', include('task_manager.label.urls')),
]
