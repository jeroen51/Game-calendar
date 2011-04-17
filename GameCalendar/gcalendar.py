import timeywimey
from datetime import datetime, timedelta
from models import Event

class CalendarMonth:
    monthName = None
    nextMonthName = None
    prevMonthName = None
    nextYear = None
    prevYear = None
    nextMonth = None
    prevMonth = None
    events = None
    
def getEventsForMonthAndYear(month, year, user):
    thisMonthStartDate = datetime(year, month, 1)

    # adding 31 days will always get a date in the next month
    nextMonthStartDate = (thisMonthStartDate + timedelta(days = 31)) 

    # subtracting 1 day will always get a date in the previous month
    prevMonthStartDate = (thisMonthStartDate - timedelta(days = 1))

    calmonth = CalendarMonth()
    calmonth.monthName = timeywimey.getmonthname(month)
    calmonth.nextYear = nextMonthStartDate.year
    calmonth.prevYear = prevMonthStartDate.year
    calmonth.nextMonth = nextMonthStartDate.month
    calmonth.prevMonth = prevMonthStartDate.month
    calmonth.nextMonthName = timeywimey.getmonthname(nextMonthStartDate.month)
    calmonth.prevMonthName = timeywimey.getmonthname(prevMonthStartDate.month) 

    events = Event.objects.filter(
            start_time__gte = thisMonthStartDate
        ).filter(
            start_time__lt = nextMonthStartDate
        ).order_by(
            'start_time'
        )

    editEvents = Event.objects.filter(
            start_time__gte = thisMonthStartDate
        ).filter(
            start_time__lt = nextMonthStartDate
        ).filter(
            acluserevent__user__id = user.id
        )

    editableEvents = filter(lambda x : x.id in (e.id for e in editEvents), events)
    
    for event in editableEvents:
        event.isEditable = True
    
    calmonth.events = events 
    return calmonth
