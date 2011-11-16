import utility, gcalendar
from django.http import HttpResponse, HttpResponseRedirect
from datetime import datetime
from django.template import Context, loader
from models import Event, News, Website, Thread
from django.core.context_processors import csrf
from django.contrib.auth.models import User
from django.contrib.auth import logout
from forms import UserForm, LoginForm
from calendarForms import EventForm

def login(request):
    error = ''

    if request.method == 'POST':
        if 'logout' in request.POST:
            logout(request)
            return HttpResponseRedirect('/')

    login_form = None
    if request.method == 'POST': 
        login_form = LoginForm(request.POST) 
        if login_form.is_valid(): 
            login_form.login(request)
    else:
        login_form = LoginForm() 

    t = loader.get_template('login.view')
    c = { 'is_authenticated' : request.user.is_authenticated(),
          'login_form' : login_form }
    c.update(csrf(request))

    return HttpResponse(t.render(Context(c)))

def index(request):
    t = loader.get_template('index.view')
    c = { 'news' : News.objects.order_by('time').reverse()[0:5],
          'links' : Website.objects.order_by('id').reverse()[0:5] }

    return HttpResponse(t.render(Context(c)))

def news(request):
    t = loader.get_template('news.view')
    c = { 'news' : News.objects.order_by('time').reverse() }
    return HttpResponse(t.render(Context(c)))

def ical(request, **args):
    t = loader.get_template('ical.view')
    
    event = None
    if 'id' in args:
        event = Event.objects.get(id = int(args['id']))

    if event:
        c = { 'event' : event, 'now' : datetime.now() }
        response =  HttpResponse(t.render(Context(c)), mimetype = "text/ical")
        response['Content-Disposition'] = 'attachment; filename="%s.ics"' % (repr(event.event_name)[2:-1]) #convert to unicode-escaped string, then strip out the escape code
        return response

def registration(request, **args):
    t = loader.get_template('registration.view')

    if request.method == 'POST': 
        register_form = UserForm(request.POST) 
        if register_form.is_valid(): 
            register_form.save(request)
            return HttpResponseRedirect('/registratie/') 
        else:
            error = register_form.errors
    else:
        register_form = UserForm() 

    c = { 'register_form' : register_form,
          'is_authenticated' : request.user.is_authenticated() }
    c.update(csrf(request))
    return HttpResponse(t.render(Context(c)))

class CalendarDay:
    def __init__(self):
        self.events = []

class GapDay:
    def __init__(self):
        self.events = []

def calendar(request, **args):
    t = loader.get_template('events.view')

    year = utility.getNrFromArgs(args, 'year', datetime.now().year)
    month = utility.getNrFromArgs(args, 'month', datetime.now().month, 
        lambda x: 0 < x < 13)

    calmonth = gcalendar.getEventsForMonthAndYear(month, year, request.user)

    #TODO: find a better way to add the threads to the event
    for event in calmonth.events:
        event.threads = Thread.objects.filter(event__id = event.id)
        for thread in event.threads:
            thread.openForEvent()

    days = {}
    for event in calmonth.events:
        if not event.start_time.day in days:
            days[event.start_time.day] = CalendarDay()
        days[event.start_time.day].events.append(event)
    
    calendarDays = []
    lastWasGapDay = False
    for i in range(32):
        if i in days:
            calendarDays.append(days[i])
            lastWasGapDay = False
        elif not lastWasGapDay:
            calendarDays.append(GapDay())
            lastWasGapDay = True
        
    c = { 'days' : calendarDays,
          'year' : year, 
          'month' : month,
          'monthname' : calmonth.monthName,
          'nextyear' : calmonth.nextYear,
          'prevyear' : calmonth.prevYear,
          'nextmonth' : calmonth.nextMonth,
          'prevmonth' : calmonth.prevMonth,
          'nextmonthname' : calmonth.nextMonthName,
          'prevmonthname' : calmonth.prevMonthName }
    return HttpResponse(t.render(Context(c)))

def addevent(request):
    error = ''

    form = None
    if request.user.is_authenticated():
        if request.method == 'POST': 
            form = EventForm(request.POST) 
            if form.is_valid(): 
                form.save(request)
                return HttpResponseRedirect('/calendar/') 
            else:
                error = form.errors
        else:
            form = EventForm() 

    t = loader.get_template('addevent.view')
    c = { 'form': form, 
          'error': error,
          'is_authenticated' : request.user.is_authenticated() }
    c.update(csrf(request))

    return HttpResponse(t.render(Context(c)))
