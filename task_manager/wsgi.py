import os
import rollbar
from django.core.wsgi import get_wsgi_application
from django.conf import settings


os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'task_manager.settings')

application = get_wsgi_application()

if settings.ROLLBAR.get('enabled', False):
    rollbar.init(**settings.ROLLBAR)
