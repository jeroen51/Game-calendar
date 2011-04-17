from django.contrib import admin
import GameCalendar.models as models

class EventAdmin(admin.ModelAdmin):
    pass

class NewsAdmin(admin.ModelAdmin):
    pass

class ThreadAdmin(admin.ModelAdmin):
    pass

class MessageAdmin(admin.ModelAdmin):
    pass

class ACLUserEventAdmin(admin.ModelAdmin):
    pass

class WebsiteAdmin(admin.ModelAdmin):
    pass

admin.site.register(models.Event, EventAdmin)
admin.site.register(models.News, NewsAdmin)
admin.site.register(models.Thread, ThreadAdmin)
admin.site.register(models.Message, MessageAdmin)
admin.site.register(models.Website, WebsiteAdmin)
admin.site.register(models.ACLUserEvent, ACLUserEventAdmin)
