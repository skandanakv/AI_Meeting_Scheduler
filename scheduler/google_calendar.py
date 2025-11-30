import streamlit as st
from google.oauth2 import service_account
from googleapiclient.discovery import build
import datetime
import pytz
import json

LOCAL_TZ = pytz.timezone("Asia/Kolkata")

SCOPES = [
    "https://www.googleapis.com/auth/calendar.readonly",  # for read-only
    "https://www.googleapis.com/auth/calendar.events"    # for creating events
]

@st.cache_resource
def get_calendar_service():
    """Get authenticated Google Calendar service using service account"""
    try:
        # Load JSON from Streamlit secrets
        creds_json = st.secrets["GOOGLE_SERVICE_ACCOUNT_JSON"]
        credentials_dict = json.loads(creds_json)
        
        # Build credentials
        credentials = service_account.Credentials.from_service_account_info(
            credentials_dict,
            scopes=SCOPES
        )
        
        # Build service (cache_discovery=False avoids SSL errors)
        service = build("calendar", "v3", credentials=credentials, cache_discovery=False)
        
        # Test connection
        service.calendarList().list(maxResults=1).execute()
        return service
    except Exception as e:
        st.error(f"❌ Calendar connection error: {str(e)}")
        return None

def get_upcoming_events(max_results=10):
    """Fetch upcoming events from your calendar"""
    service = get_calendar_service()
    if not service:
        return []
    
    try:
        now = datetime.datetime.utcnow().isoformat() + "Z"
        events_result = service.events().list(
            calendarId="primary",
            timeMin=now,
            maxResults=max_results,
            singleEvents=True,
            orderBy="startTime"
        ).execute()
        events = events_result.get("items", [])
        
        # Convert start/end to LOCAL_TZ datetime
        formatted_events = []
        for ev in events:
            start = ev["start"].get("dateTime")
            end = ev["end"].get("dateTime")
            if start and end:
                start_dt = datetime.datetime.fromisoformat(start.replace("Z", "+00:00")).astimezone(LOCAL_TZ)
                end_dt = datetime.datetime.fromisoformat(end.replace("Z", "+00:00")).astimezone(LOCAL_TZ)
                formatted_events.append({
                    "summary": ev.get("summary", "No Title"),
                    "start": start_dt,
                    "end": end_dt
                })
        return formatted_events
    except Exception as e:
        st.error(f"Error fetching events: {str(e)}")
        return []

def get_events_in_range(start, end):
    """Fetch events in a specific date range"""
    service = get_calendar_service()
    if not service:
        return []

    try:
        events_result = service.events().list(
            calendarId="primary",
            timeMin=start.astimezone(pytz.UTC).isoformat(),
            timeMax=end.astimezone(pytz.UTC).isoformat(),
            singleEvents=True,
            orderBy="startTime"
        ).execute()

        events = []
        for ev in events_result.get("items", []):
            s = ev["start"].get("dateTime")
            e = ev["end"].get("dateTime")
            if not s or not e:
                continue
            s_dt = datetime.datetime.fromisoformat(s.replace("Z", "+00:00")).astimezone(LOCAL_TZ)
            e_dt = datetime.datetime.fromisoformat(e.replace("Z", "+00:00")).astimezone(LOCAL_TZ)
            events.append({
                "summary": ev.get("summary", "No Title"),
                "start": s_dt,
                "end": e_dt
            })
        return events
    except Exception as e:
        st.error(f"Error fetching events in range: {str(e)}")
        return []

def create_event(summary, start_datetime, end_datetime, description="", attendees=None):
    """Create a new event on the calendar"""
    service = get_calendar_service()
    if not service:
        return None

    try:
        event_body = {
            "summary": summary,
            "description": description,
            "start": {
                "dateTime": start_datetime.isoformat(),
                "timeZone": "Asia/Kolkata"
            },
            "end": {
                "dateTime": end_datetime.isoformat(),
                "timeZone": "Asia/Kolkata"
            }
        }

        if attendees:
            event_body["attendees"] = [{"email": a} for a in attendees]

        event = service.events().insert(calendarId="primary", body=event_body).execute()
        return event
    except Exception as e:
        st.error(f"Error creating event: {str(e)}")
        return None
