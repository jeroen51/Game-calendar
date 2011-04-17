from django.db import models
from django.contrib.auth.models import User

class Event(models.Model):
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    event_name = models.CharField(max_length=400)
    event_description = models.TextField()
    event_location = models.CharField(max_length=5000)
    event_organizer = models.CharField(max_length=400)
    
    def __str__(self):
        return self.event_name

class News(models.Model):
    time = models.DateTimeField()
    description = models.TextField()

    def __str__(self):
        return self.time.strftime('%d-%m-%Y %H:%M:%S')

class Thread(models.Model):
    time = models.DateTimeField()
    event = models.ForeignKey(Event)
    user = models.ForeignKey(User)
    title = models.CharField(max_length=400)
    description = models.TextField()

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

class Website(models.Model):
    name = models.CharField(max_length=400)
    url = models.CharField(max_length=400)

    def __str__(self):
        return self.name
