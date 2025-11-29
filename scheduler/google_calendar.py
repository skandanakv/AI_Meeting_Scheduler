import os
import json
import datetime
import pytz
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Paths
CREDENTIALS_PATH = "credentials/client_secret.json"
TOKEN_PATH = "credentials/token.json"

# Scopes
SCOPES = [
    'https://www.googleapis.com/auth/calendar.events',
    'https://www.googleapis.com/auth/calendar.readonly'
]

# Timezone (India)
LOCAL_TZ = pytz.timezone('Asia/Kolkata')


def get_calendar_service():
    """Authenticate and return Google Calendar API service."""
    creds = None

    if os.path.exists(TOKEN_PATH):
        creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
            except:
                creds = None

        if not creds:
            if not os.path.exists(CREDENTIALS_PATH):
                raise FileNotFoundError(
                    f"Missing Google OAuth file at {CREDENTIALS_PATH}"
                )
            flow = InstalledAppFlow.from_client_secrets_file(
                CREDENTIALS_PATH, SCOPES
            )
            creds = flow.run_local_server(port=0)

        with open(TOKEN_PATH, 'w') as token:
            token.write(creds.to_json())

    return build('calendar', 'v3', credentials=creds)


def get_upcoming_events(max_results=10):
    """Fetch upcoming events from Google Calendar."""
    try:
        service = get_calendar_service()
        now = datetime.datetime.utcnow().isoformat() + 'Z'  # UTC

        events_result = service.events().list(
            calendarId='primary',
            timeMin=now,
            maxResults=max_results,
            singleEvents=True,
            orderBy='startTime'
        ).execute()

        return events_result.get('items', [])

    except HttpError:
        return []


def get_events_in_range(start_datetime, end_datetime):
    """Return events in a specific time interval."""
    try:
        service = get_calendar_service()

        time_min = start_datetime.astimezone(pytz.UTC).isoformat()
        time_max = end_datetime.astimezone(pytz.UTC).isoformat()

        events_result = service.events().list(
            calendarId="primary",
            timeMin=time_min,
            timeMax=time_max,
            singleEvents=True,
            orderBy='startTime'
        ).execute()

        events_list = []

        for event in events_result.get('items', []):
            start = event['start'].get('dateTime')
            end = event['end'].get('dateTime')

            start_dt = datetime.datetime.fromisoformat(start.replace('Z', '+00:00'))
            end_dt = datetime.datetime.fromisoformat(end.replace('Z', '+00:00'))

            events_list.append({
                'summary': event.get('summary', 'Untitled'),
                'start': start_dt.astimezone(LOCAL_TZ),
                'end': end_dt.astimezone(LOCAL_TZ),
                'id': event.get('id')
            })

        return events_list

    except HttpError:
        return []


def get_busy_times(start_datetime, end_datetime):
    """Return busy time slots using FreeBusy API."""
    try:
        service = get_calendar_service()

        time_min = start_datetime.astimezone(pytz.UTC).isoformat()
        time_max = end_datetime.astimezone(pytz.UTC).isoformat()

        body = {
            "timeMin": time_min,
            "timeMax": time_max,
            "items": [{"id": "primary"}]
        }

        freebusy_result = service.freebusy().query(body=body).execute()
        busy_times = freebusy_result['calendars']['primary']['busy']

        results = []
        for slot in busy_times:
            start = datetime.datetime.fromisoformat(slot['start'].replace('Z', '+00:00'))
            end = datetime.datetime.fromisoformat(slot['end'].replace('Z', '+00:00'))

            results.append({
                'start': start.astimezone(LOCAL_TZ),
                'end': end.astimezone(LOCAL_TZ)
            })

        return results

    except HttpError:
        return []


def create_event(summary, start_datetime, end_datetime, description="", attendees=None):
    """
    Create a calendar event with correct time (timezone-safe).
    FIXED: No "timeZone" field → prevents Google shifting time to 7:30 PM.
    """
    try:
        service = get_calendar_service()

        event = {
            "summary": summary,
            "description": description,
            "start": {
                "dateTime": start_datetime.isoformat(),  # timezone included already
            },
            "end": {
                "dateTime": end_datetime.isoformat(),
            }
        }

        if attendees:
            event["attendees"] = [{"email": email} for email in attendees]

        created_event = service.events().insert(
            calendarId="primary",
            body=event
        ).execute()

        return created_event

    except HttpError as e:
        print(f"Error creating event: {e}")
        return None


def test_calendar_connection():
    """Simple diagnostic test."""
    print("\n=== Testing Google Calendar API ===")

    try:
        svc = get_calendar_service()
        print("✓ Authenticated successfully!")

        events = get_upcoming_events(3)
        print(f"Fetched {len(events)} upcoming events.")

        now = datetime.datetime.now(LOCAL_TZ)
        busy = get_busy_times(now, now + datetime.timedelta(days=7))
        print(f"Busy slots this week: {len(busy)}")

        print("✓ All tests passed!")

    except Exception as e:
        print("✗ Test failed:", e)


if __name__ == "__main__":
    test_calendar_connection()
