from django.template import Context, loader
from django.http import HttpResponse, HttpResponseRedirect
from models import Thread, Message

def thread(request, **args):
    t = loader.get_template('discussion.view') 
    thread = None
    if 'id' in args:
        thread = Thread.objects.get(id = int(args['id']))

    c = { 'thread' : thread,
          'messages' : None }

    if thread:
        messages = Message.objects.filter(thread__id = thread.id)
        c['messages'] = messages
    return HttpResponse(t.render(Context(c)))
