from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView

from .views import UserSignIn, logout_view


urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', UserSignIn.as_view(), name='signin'),
    path('logout/', logout_view, name='signout'),
    path('', TemplateView.as_view(template_name='index.html'), name='home'),
    path('users/', include('task_manager.user.urls')),
    path('statuses/', include('task_manager.status.urls')),
]
