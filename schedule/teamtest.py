from datetime import date, datetime, timedelta
import http.client
import json
import os

today = date.today()
# Show events for next two weeks
delta = timedelta(days=14)
two_weeks = today + delta
formatted_today = today.strftime("%Y-%m-%d")
formatted_two_weeks = two_weeks.strftime("%Y-%m-%d")

conn = http.client.HTTPSConnection("api.teamup.com")
print(conn)

# USE ENVIRONMENT VARIABLES #
headers = {
  'Accept': "application/json",
  'Teamup-Token': os.getenv("TEAMUP_TOKEN"), 
  'Teamup-Password': os.getenv("TEAMUP_PASS"),
}

conn.request("GET", f"/ksns7tb5ichjhm51wh/events?startDate={formatted_today}&endDate={formatted_two_weeks}&tz=America/London", headers=headers)

res = conn.getresponse()
data = res.read()

# Save as a string
with open("calendar_response.json", "w") as f:
  json.dump(data.decode("utf-8"), f)
  