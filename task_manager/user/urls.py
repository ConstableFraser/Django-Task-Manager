from django.urls import path

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
    path('<int:pk>',
         views.UserDetailView.as_view(),
         name='user_card'),
]
