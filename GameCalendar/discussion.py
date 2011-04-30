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
    
    if thread and thread.openForEvent():
        if request.method == 'POST': 
            # Post dictionary needs to be mutable in order to remove the value from the messagebox
            post_vars = {}
            for key in request.POST:
                post_vars[key] = request.POST[key]

            message_form = MessageForm(post_vars) 
            if message_form.is_valid(): 
                message = Message()
                message.content = message_form.cleaned_data['content']
                message_form.data['content'] = ''
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
