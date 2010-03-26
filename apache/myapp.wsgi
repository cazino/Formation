
import os
import sys

os.environ['DJANGO_SETTINGS_MODULE'] = 'greta.settings'

sys.path.append('/var/www/vhosts/gestmve.org/django')
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()

