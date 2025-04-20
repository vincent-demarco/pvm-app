from datetime import date
from django.db import models

class ClanMember(models.Model):
  name = models.CharField(max_length=20, unique=True)

  def __str__(self):
    return self.name
  
  class Meta:
    ordering = ["name"]
  
class Event(models.Model):
  title = models.CharField(max_length=50) # E.g. Graardor, Kerapac, KBD, etc
  date = models.DateField(default=date.today)
  participants = models.ManyToManyField(ClanMember)
  points = models.IntegerField(default=50) # Points this event is worth
  completed = models.BooleanField(default=False) 

  def __str__(self):
    return self.title

  def participant_names(self):
    return ', '.join([a.name for a in self.participants.all()])

