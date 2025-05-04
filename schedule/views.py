from datetime import datetime, timedelta
import json
import os
from django.shortcuts import render
import requests

# Lookup table for get_calendar_data()
categories = {
    14139620: "Clan Event",
    14139621: "PvM Event",
    14139634: "Minigames/D&D",
    14139645: "Jagex Events",
}

def get_calendar_data():
  # App Platform doesn't support cron jobs, so I'm running one on my personal
  # site's server instead. It should execute every day as of May 3 2025, may 
  # change it to something more regular in the future.
  #
  # This function pulls the json from my personal site and creates an array of
  # event objects for the schedule.html template to display.

  response = requests.get("https://josephdemarco.xyz/calendar_response.json")
  data = response.json()
  
  # Reencode the string to work with it as a JSON Object
  response_dict = json.loads(data)

  class CalendarEvent:
      def __init__(self, title, start, end, category):
          self.title = title
          self.start = start
          self.end = end
          self.category = category

  calendarEvents = []

  for event in response_dict.get("events", []):
      # The TeamUp calendar is inputted in -11:00 (EST?) even though it's meant to 
      # represent UTC, so we have to adjust the times by 7 hours. 
      delta = timedelta(hours=7)
      title = event['title']
      all_day = event['all_day']

      # ISO
      start = event['start_dt']
      end = event['end_dt']
      category = categories.get(event['subcalendar_id'], "Unknown")

      # Datetime objects
      # .strftime("%B %d %H:%M UTC")
      start_dt = datetime.fromisoformat(start)
      end_dt = datetime.fromisoformat(end)

      # "UTC datetime" objects. All day and normal aren't comparable after this step.
      # Look into changing the timezone stamp instead. See Pages doc.
      if not all_day:
        start_utc = start_dt + delta
        end_utc = end_dt + delta
      else:
        start_utc = start_dt
        end_utc = end_dt

      # String objects
      start_form = start_utc.strftime("%B %d %H:%M UTC")
      end_form = end_utc.strftime("%B %d %H:%M UTC")


      # Create new event object
      newEvent = CalendarEvent(title, start_form, end_form, category)

      # Add event to array. This should be the context for the calendar_view.
      calendarEvents.append(newEvent)

  # Sort by start date. String sort.
  sortedCalendar = sorted(calendarEvents, key=lambda event: event.start)
  return sortedCalendar

def calendar_view(request):
  return render(request, "schedule/schedule.html", {
     "calendar_list": get_calendar_data(),
  })