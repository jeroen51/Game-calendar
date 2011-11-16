from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
    (r'^nieuws/?', 'GameCalendar.home.news'),
    (r'^news/?', 'GameCalendar.home.news'),
    (r'^discussion/(?P<id>\d+)/?', 'GameCalendar.discussion.thread'),
    (r'^discussie/(?P<id>\d+)/?', 'GameCalendar.discussion.thread'),
    (r'^registration/?', 'GameCalendar.home.registration'),
    (r'^registratie/?', 'GameCalendar.home.registration'),
    (r'^event/(?P<id>\d+)/?', 'GameCalendar.eventcontrol.eventDetails'),
    (r'^evenement/(?P<id>\d+)/?', 'GameCalendar.eventcontrol.eventDetails'),
    (r'^add_event/?', 'GameCalendar.home.addevent'),
    (r'^evenement_toevoegen/?', 'GameCalendar.home.addevent'),
    (r'^ical/(?P<id>\d+)/?', 'GameCalendar.home.ical'),
    (r'^over/?', 'GameCalendar.home.index'),
    (r'^about/?', 'GameCalendar.home.index'),
    (r'^inloggen/?', 'GameCalendar.home.login'),
    (r'^login/?', 'GameCalendar.home.login'),
    (r'^kalender/(?P<year>\d+)/(?P<month>\d+)/?', 'GameCalendar.home.calendar'),
    (r'^calendar/(?P<year>\d+)/(?P<month>\d+)/?', 'GameCalendar.home.calendar'),
    (r'^kalender/(?P<year>\d+)/?', 'GameCalendar.home.calendar'),
    (r'^calendar/(?P<year>\d+)/?', 'GameCalendar.home.calendar'),
    (r'^kalender/?', 'GameCalendar.home.calendar'),
    (r'^calendar/?', 'GameCalendar.home.calendar'),
    (r'', 'GameCalendar.home.calendar')
)
