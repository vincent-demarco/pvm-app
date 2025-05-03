from datetime import datetime
import json

# Lookup table
categories = {
    14139620: "Clan Event",
    14139621: "PvM Event",
    14139634: "Minigames/D&D",
    14139645: "Jagex Events",
}

# Load saved string from scheduled job
with open("calendar_response.json", "r") as f:
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
    start_dt = datetime.fromisoformat(start).strftime("%d-%m-%Y %H:%M:%S")
    end_dt = datetime.fromisoformat(end).strftime("%d-%m-%Y %H:%M:%S")

    # Create new event object
    newEvent = CalendarEvent(title, start_dt, end_dt, category)

    # Add event to array. This should be the context for the calendar_view.
    calendarEvents.append(newEvent)
    
# print(calendarEvents)