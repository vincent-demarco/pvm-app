from django import forms
from django.contrib import admin
from django.forms.widgets import CheckboxSelectMultiple

from . import models

class EventForm(forms.ModelForm):
  class Meta:
    model = models.Event
    fields = '__all__'
    widgets = {
      'participants': CheckboxSelectMultiple(),
    }

# Register your models here.
class EventAdmin(admin.ModelAdmin):
  list_display = ["title", "date", "completed"]
  form = EventForm

class MemberAdmin(admin.ModelAdmin):
  pass

admin.site.register(models.Event, EventAdmin)
admin.site.register(models.ClanMember, MemberAdmin)