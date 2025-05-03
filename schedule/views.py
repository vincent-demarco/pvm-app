from datetime import datetime
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
  # A cron job is set up to run teamtest.py every day
  # The results are stored in a file
  # This function reads the results out of the file and formats it for the 
  # view context.
  # Load saved string from scheduled job
  file_path = os.path.join(os.path.dirname(__file__), "calendar_response.json")
  with open(file_path, "r") as f:
      data = json.load(f)

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
      title = event['title']
      start = event['start_dt']
      end = event['end_dt']
      category = categories.get(event['subcalendar_id'], "Unknown")

      # Convert 08-05-2023 18:00:00 format
      start_dt = datetime.fromisoformat(start).strftime("%B %d %H:%M UTC")
      end_dt = datetime.fromisoformat(end).strftime("%B %d %H:%M UTC")

      # Create new event object
      newEvent = CalendarEvent(title, start_dt, end_dt, category)

      # Add event to array. This should be the context for the calendar_view.
      calendarEvents.append(newEvent)

  return calendarEvents

def calendar_view(request):
  return render(request, "schedule/schedule.html", {
     "calendar_list": get_calendar_data(),
  })