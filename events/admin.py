from django.contrib import admin

from . import models

# Register your models here.
class EventAdmin(admin.ModelAdmin):
  list_display = ["title", "date", "completed"]

class MemberAdmin(admin.ModelAdmin):
  pass

admin.site.register(models.Event, EventAdmin)
admin.site.register(models.ClanMember, MemberAdmin)