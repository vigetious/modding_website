import os
import django
os.environ['DJANGO_SETTINGS_MODULE'] = 'mysite.settings'
django.setup()

# This application object is used by the development server
# as well as any WSGI server configured to use this file.
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()