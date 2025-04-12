from datetime import date
from django.db import models


# Create your models here.

# A model class represents a database table

class ClanMember(models.Model):
  name = models.CharField(max_length=20)
  # current_points = models.IntegerField(default=0) 
  # bonus_points = models.IntegerField(default=0) # For going above & beyond


  def __str__(self):
    return self.name
  
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

