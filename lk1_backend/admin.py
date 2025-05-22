from django.contrib import admin
from .models import *

admin.site.register(UserProfile)
admin.site.register(UserRole)
admin.site.register(UserFile)
admin.site.register(Skill)
admin.site.register(Direction)
admin.site.register(Project)
admin.site.register(UserProject)
admin.site.register(Meeting)
admin.site.register(UserMeeting)
admin.site.register(Event)
admin.site.register(UserEvent)
admin.site.register(EventDirection)
admin.site.register(ApllictationToEvent)
admin.site.register(ApllictationToProject)
