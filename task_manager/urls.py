"""urls.py module for the task manager app."""
from django.contrib import admin
from django.urls import path, include
from . import views
from task_manager.views import test_rollbar

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index_view, name='home'),
    path('users/', include('task_manager.users.urls')),
    path('statuses/', include('task_manager.statuses.urls')),
    path('labels/', include('task_manager.labels.urls')),
    path('tasks/', include('task_manager.tasks.urls')),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('test-rollbar/', test_rollbar, name='test_rollbar'),
]
