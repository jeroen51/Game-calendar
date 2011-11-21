from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, timedelta
from django.utils.translation import ugettext as _

class News(models.Model):
    time = models.DateTimeField()
    description = models.TextField()

    def __str__(self):
        return self.time.strftime('%d-%m-%Y %H:%M:%S')

class Event(models.Model):
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    event_name = models.CharField(max_length=400)
    event_description = models.TextField()
    event_location = models.CharField(max_length=5000)
    event_organizer = models.CharField(max_length=400)
    event_website = models.CharField(max_length=250)
    isEditable = False
    
    def __str__(self):
        return self.event_name

    def loadThreads(self):
        self.threads = Thread.objects.filter(event__id = self.id).order_by('title')
        for thread in self.threads:
            thread.openForEvent()

class Thread(models.Model):
    #Silly English doesn't have decent words for this:
    #   - Pre-discussion: before the event takes place
    #   - Post-discussion: after the event takes place
    #   - Live discussion: while the event takes place
    THREAD_TYPES = (
        ('PR', 'Pre-discussion'),
        ('PO', 'Post-discussion'),
        ('LI', 'Live discussion'),
    )

    time = models.DateTimeField()
    event = models.ForeignKey(Event)
    thread_type = models.CharField(max_length=2, choices=THREAD_TYPES)
    user = models.ForeignKey(User)
    title = models.CharField(max_length=400)
    description = models.TextField()
    closed = True

    def openForEvent(self):
        """The same as getStatus, but returns a simple boolean value."""
        return self.getStatus() == 'open'

    def getStatus(self):
        """Returns the discussion status as a string. Values are: 'early', 'late' and 'open'"""
        
        start = {
                    'PO' : self.event.end_time,
                    'LI' : self.event.start_time
                }
        end = {
                'PR' : self.event.start_time + timedelta(hours=3),
                'LI' : self.event.end_time + timedelta(hours=3)
              }
        if self.thread_type in start and datetime.now() < start[self.thread_type]:
            self.closed = True
            return 'early'
        if self.thread_type in end and datetime.now() > end[self.thread_type]:
            self.closed = True
            return 'late'
        self.closed = False
        return 'open' 

    def getStatusMessage(self):
        current_status = self.getStatus()
        if current_status == 'early':
            return _("Sorry, the discussion hasn't opened yet. Check back later.")
        if current_status == 'late':
            return _("The discussion has already been closed. Feel free to read the old comments")
        return _("The discussion is open, feel free to participate.")

    def __str__(self):
        return self.title

class Message(models.Model):
    time = models.DateTimeField()
    content = models.TextField()
    thread = models.ForeignKey(Thread)
    user = models.ForeignKey(User)

    def __str__(self):
        return self.time.strftime('%d-%m-%Y %H:%M:%S') + ': ' + `self.user`

class ACLUserEvent(models.Model):
    user = models.ForeignKey(User)
    event = models.ForeignKey(Event)
    
    def __str__(self):
        return `self.user` + ' - ' + `self.event`

class Presence(models.Model):
    PRESENTNESS_TYPES = (
        ('PR', 'Present'),
        ('AB', 'Absent')
    )

    user = models.ForeignKey(User)
    event = models.ForeignKey(Event)
    presentness = models.CharField(max_length=2, choices=PRESENTNESS_TYPES)
    reason = models.TextField()

    def __str__(self):
        return `self.user` + ' - ' + `self.event` + ' - ' + `self.presentness`

class Website(models.Model):
    name = models.CharField(max_length=400)
    url = models.CharField(max_length=400)

    def __str__(self):
        return self.name
