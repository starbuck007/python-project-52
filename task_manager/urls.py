"""urls.py module for the task manager app."""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns
from . import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index_view, name='home'),
    path('users/', include('task_manager.users.urls')),
    path('statuses/', include('task_manager.statuses.urls')),
    path('labels/', include('task_manager.labels.urls')),
    path('tasks/', include('task_manager.tasks.urls')),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('i18n/', include('django.conf.urls.i18n')),
]

urlpatterns += i18n_patterns(
    path('', views.index_view, name='home'),
    path('statuses/', include('task_manager.statuses.urls')),
    path('labels/', include('task_manager.labels.urls')),
    path('tasks/', include('task_manager.tasks.urls')),
    path('users/', include('task_manager.users.urls')),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    prefix_default_language=False,
)
