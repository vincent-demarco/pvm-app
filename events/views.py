from django.db.models.functions import ExtractMonth, ExtractYear
from django.utils.timezone import now
from django.shortcuts import render

from .models import Event

# Tally points for each player who has participated in this month's events.
def tally_points():
  today = now()
  current_month = today.month
  current_year = today.year

  standings_dict = {}

  # Get completed events this month
  completed_events_this_month = Event.objects.annotate(
      month=ExtractMonth('date'),
      year=ExtractYear('date')
  ).filter(month=current_month, year=current_year).filter(completed=True)

  # For each player who has participated in at least 1 event, add up the points
  # for each event they have completed this month. 
  for event in completed_events_this_month:
    for player in event.participants.all():
      if standings_dict.get(player.name):
        standings_dict[player.name] += event.points
      else:
        standings_dict[player.name] = event.points

  # Return a dictionary of {player, points}, sorted by points in descending
  # order. 
  return dict(sorted(standings_dict.items(), key=lambda item: item[1], reverse=True))

def CurrentMonthView(request):
  event_list = Event.objects.filter(completed=False)
  return render(request, "events/current.html", {
    "event_list": event_list,
    "sorted_standings": tally_points(),
  })


