import os, sys
sys.path.append('/var/www/spelkalender')

os.environ['DJANGO_SETTINGS_MODULE'] = 'GameCalendar.settings'

import django.core.handlers.wsgi

application = django.core.handlers.wsgi.WSGIHandler()
