from models import Event
from django.core.context_processors import csrf
from django.http import HttpResponse, HttpResponseRedirect
from django.template import Context, loader

def eventDetails(request, **args):
    t = loader.get_template('eventdetails.view')

    user = request.user
    
    c = { 'event' : None, 'is_authenticated' : False }
    c.update(csrf(request))

    if not user.is_authenticated():
        return HttpResponse(t.render(Context(c)))
    else:
        c['is_authenticated'] = True

    event = None
    if 'id' in args:
        event = Event.objects.filter(acluserevent__user__id = user.id).get(id = int(args['id']))

    if event:
        c['event'] = event

    if event and 'delete' in request.POST:
        event.delete()
        return HttpResponseRedirect('/kalender/')
    
    return HttpResponse(t.render(Context(c)))
            
