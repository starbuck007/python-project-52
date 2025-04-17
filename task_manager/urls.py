from django.contrib import admin
from django.urls import path
from .views import (index_view, UserListView, UserCreateView, UserUpdateView,
                    UserDeleteView, login_view, logout_view)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index_view, name='home'),
    path('users/', UserListView.as_view(), name='user_list'),
    path('users/create/', UserCreateView.as_view(), name='user_create'),
    path('users/<int:pk>/update/', UserUpdateView.as_view(), name='user_update'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('users/<int:pk>/delete/', UserDeleteView.as_view(), name='user_delete'),
]
