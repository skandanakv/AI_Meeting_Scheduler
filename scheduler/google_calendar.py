import streamlit as st
from google.oauth2 import service_account
from googleapiclient.discovery import build
import datetime
import pytz
import json

LOCAL_TZ = pytz.timezone("Asia/Kolkata")

SCOPES = [
    'https://www.googleapis.com/auth/calendar.readonly',
    'https://www.googleapis.com/auth/calendar.events'
]


@st.cache_resource
def get_calendar_service():
    """Get authenticated Google Calendar service using service account"""
    try:
        credentials_dict = json.loads(st.secrets["GOOGLE_SERVICE_ACCOUNT_JSON"])
        
        credentials = service_account.Credentials.from_service_account_info(
            credentials_dict,
            scopes=SCOPES
        )
        
        service = build('calendar', 'v3', credentials=credentials)
        return service
    except Exception as e:
        st.error(f"Error connecting to Google Calendar: {str(e)}")
        return None


def get_upcoming_events(max_results=10):
    """Fetch upcoming events"""
    service = get_calendar_service()
    if not service:
        return []
    
    try:
        now = datetime.datetime.utcnow().isoformat() + 'Z'
        
        events_result = service.events().list(
            calendarId='primary',
            timeMin=now,
            maxResults=max_results,
            singleEvents=True,
            orderBy='startTime'
        ).execute()
        
        return events_result.get('items', [])
    except Exception as e:
        st.error(f"Error fetching events: {str(e)}")
        return []


def get_events_in_range(start, end):
    """Fetch events in specific date range"""
    service = get_calendar_service()
    if not service:
        return []
    
    try:
        events_result = service.events().list(
            calendarId='primary',
            timeMin=start.astimezone(pytz.UTC).isoformat(),
            timeMax=end.astimezone(pytz.UTC).isoformat(),
            singleEvents=True,
            orderBy='startTime'
        ).execute()
        
        events = []
        for ev in events_result.get('items', []):
            s = ev['start'].get('dateTime')
            e = ev['end'].get('dateTime')
            
            if not s or not e:
                continue
            
            s_dt = datetime.datetime.fromisoformat(s.replace('Z', '+00:00')).astimezone(LOCAL_TZ)
            e_dt = datetime.datetime.fromisoformat(e.replace('Z', '+00:00')).astimezone(LOCAL_TZ)
            
            events.append({
                'summary': ev.get('summary'),
                'start': s_dt,
                'end': e_dt
            })
        
        return events
    except Exception as e:
        st.error(f"Error fetching events: {str(e)}")
        return []


def get_busy_times(start, end):
    """Get busy time slots from calendar events"""
    events = get_events_in_range(start, end)
    busy_times = []
    
    for event in events:
        busy_times.append({
            'start': event['start'],
            'end': event['end']
        })
    
    return busy_times


def create_event(summary, start_datetime, end_datetime, description="", attendees=None):
    """Create a new event"""
    service = get_calendar_service()
    if not service:
        return None
    
    try:
        event_body = {
            'summary': summary,
            'description': description,
            'start': {
                'dateTime': start_datetime.isoformat(),
                'timeZone': 'Asia/Kolkata'
            },
            'end': {
                'dateTime': end_datetime.isoformat(),
                'timeZone': 'Asia/Kolkata'
            }
        }
        
        if attendees:
            event_body['attendees'] = [{'email': a} for a in attendees]
        
        event = service.events().insert(
            calendarId='primary',
            body=event_body
        ).execute()
        
        return event
    except Exception as e:
        st.error(f"Error creating event: {str(e)}")
        return None