from models import Event
from django.core.context_processors import csrf
from django.http import HttpResponse, HttpResponseRedirect
from django.template import Context, loader
from django.core.exceptions import ObjectDoesNotExist

def eventDetails(request, **args):
    t = loader.get_template('eventdetails.view')

    user = request.user
    
    c = { 'event' : None, 'can_delete' : False }
    c.update(csrf(request))

    event = None
    if 'id' in args:
        event = Event.objects.get(id = int(args['id']))
        event.loadThreads()

    if event:
        c['event'] = event
        c['can_delete'] = can_delete(user, args)

    if event and 'delete' in request.POST and can_delete(user):
        event.delete()
        return HttpResponseRedirect('/kalender/')
    
    return HttpResponse(t.render(Context(c)))

def can_delete(user, args):
    try:
        return user.is_authenticated() and Event.objects.filter(acluserevent__user__id = user.id).get(id = int(args['id']))
    except ObjectDoesNotExist:
        return False
