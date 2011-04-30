from django import forms
from models import Event, Thread, ACLUserEvent
from django.contrib.auth.models import User
from datetime import datetime
from django.utils.translation import ugettext as _

class EventForm(forms.Form):
    start_date = forms.DateField()
    end_date = forms.DateField()
    start_time = forms.TimeField()
    end_time = forms.TimeField()
    event_name = forms.CharField(max_length=400)
    event_location = forms.CharField(max_length=5000, widget=forms.Textarea)
    event_organizer = forms.CharField(max_length=5000)
    event_description = forms.CharField(max_length=20000, widget=forms.Textarea)

    def save(self, request):
        event = Event()
        start_date = self.cleaned_data['start_date']
        end_date = self.cleaned_data['end_date']
        start_time = self.cleaned_data['start_time']
        end_time = self.cleaned_data['end_time']
        event.start_time = datetime.combine(start_date, start_time)
        event.end_time = datetime.combine(end_date, end_time)
        event.event_name = self.cleaned_data['event_name']
        event.event_location = self.cleaned_data['event_location']
        event.event_organizer = self.cleaned_data['event_organizer']
        event.event_description = self.cleaned_data['event_description']
        event.save()

        acl = ACLUserEvent()
        acl.user = request.user
        acl.event = event
        acl.save()

        discussiondefs = (
                            ('PR', _(u'Discussion of the upcoming %s'), _(u'Discuss the upcoming event %s before it actually happens.')), 
                            ('LI', _(u'Live discussion of %s'), _(u'Discuss the ongoing event %s live.')),
                            ('PO', _(u'Post-hoc discussion of %s'), _(u'Discuss %s after the facts.'))
                         )

        for s in discussiondefs:
            thread = Thread()
            thread.time = datetime.now()
            thread.user = request.user
            thread.event = event
            thread.thread_type = s[0];
            thread.title = s[1] % (event.event_name)
            thread.description = s[2] % (event.event_name)
            thread.save()

