from django.template import Context, loader
from django.http import HttpResponse, HttpResponseRedirect
from django.core.context_processors import csrf
from models import Thread, Message
from forms import MessageForm
from datetime import datetime

def thread(request, **args):
    t = loader.get_template('discussion.view') 
    thread = None
    if 'id' in args:
        thread = Thread.objects.get(id = int(args['id']))

    message_form = None
    if thread:
        if request.method == 'POST': 
            message_form = MessageForm(request.POST) 
            if message_form.is_valid(): 
                message = Message()
                message.content = message_form.cleaned_data['content']
                message.time = datetime.now()
                message.user = request.user
                message.thread = thread
                message.save()
        else:
            message_form = MessageForm()

    c = { 'thread' : thread,
          'messages' : None,
          'message_form' : message_form,
          'is_authenticated' : request.user.is_authenticated()
        }

    if thread:
        messages = Message.objects.filter(thread__id = thread.id)
        c['messages'] = messages

    c.update(csrf(request))
    return HttpResponse(t.render(Context(c)))
