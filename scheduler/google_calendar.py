# import streamlit as st
# from google.oauth2 import service_account
# from googleapiclient.discovery import build
# import datetime
# import pytz
# import json

# LOCAL_TZ = pytz.timezone("Asia/Kolkata")

# SCOPES = [
#     'https://www.googleapis.com/auth/calendar.readonly',
#     'https://www.googleapis.com/auth/calendar.events'
# ]


# @st.cache_resource
# def get_calendar_service():
#     """Get authenticated Google Calendar service using service account"""
#     try:
#         creds_json = st.secrets["GOOGLE_SERVICE_ACCOUNT_JSON"]
#         credentials_dict = json.loads(creds_json)
        
#         credentials = service_account.Credentials.from_service_account_info(
#             credentials_dict,
#             scopes=SCOPES
#         )
        
#         service = build('calendar', 'v3', credentials=credentials, cache_discovery=False)
#         service.calendarList().list(maxResults=1).execute()
        
#         return service
        
#     except Exception as e:
#         st.error(f"❌ Calendar connection error: {str(e)}")
#         return None


# def get_upcoming_events(max_results=10):
#     """Fetch upcoming events"""
#     service = get_calendar_service()
#     if not service:
#         return []
    
#     try:
#         now = datetime.datetime.utcnow().isoformat() + 'Z'
        
#         events_result = service.events().list(
#             calendarId='primary',
#             timeMin=now,
#             maxResults=max_results,
#             singleEvents=True,
#             orderBy='startTime'
#         ).execute()
        
#         return events_result.get('items', [])
#     except Exception as e:
#         st.error(f"Error fetching events: {str(e)}")
#         return []


# def get_events_in_range(start, end):
#     """Fetch events in specific date range"""
#     service = get_calendar_service()
#     if not service:
#         return []
    
#     try:
#         events_result = service.events().list(
#             calendarId='primary',
#             timeMin=start.astimezone(pytz.UTC).isoformat(),
#             timeMax=end.astimezone(pytz.UTC).isoformat(),
#             singleEvents=True,
#             orderBy='startTime'
#         ).execute()
        
#         events = []
#         for ev in events_result.get('items', []):
#             s = ev['start'].get('dateTime')
#             e = ev['end'].get('dateTime')
            
#             if not s or not e:
#                 continue
            
#             s_dt = datetime.datetime.fromisoformat(s.replace('Z', '+00:00')).astimezone(LOCAL_TZ)
#             e_dt = datetime.datetime.fromisoformat(e.replace('Z', '+00:00')).astimezone(LOCAL_TZ)
            
#             events.append({
#                 'summary': ev.get('summary'),
#                 'start': s_dt,
#                 'end': e_dt
#             })
        
#         return events
#     except Exception as e:
#         st.error(f"Error fetching events: {str(e)}")
#         return []


# def get_busy_times(start, end):
#     """Get busy time slots from calendar events"""
#     events = get_events_in_range(start, end)
#     busy_times = []
    
#     for event in events:
#         busy_times.append({
#             'start': event['start'],
#             'end': event['end']
#         })
    
#     return busy_times


# def create_event(summary, start_datetime, end_datetime, description="", attendees=None):
#     """Create a new event"""
#     service = get_calendar_service()
#     if not service:
#         return None
    
#     try:
#         event_body = {
#             'summary': summary,
#             'description': description,
#             'start': {
#                 'dateTime': start_datetime.isoformat(),
#                 'timeZone': 'Asia/Kolkata'
#             },
#             'end': {
#                 'dateTime': end_datetime.isoformat(),
#                 'timeZone': 'Asia/Kolkata'
#             }
#         }
        
#         if attendees:
#             event_body['attendees'] = [{'email': a} for a in attendees]
        
#         event = service.events().insert(
#             calendarId='primary',
#             body=event_body
#         ).execute()
        
#         return event
#     except Exception as e:
#         st.error(f"Error creating event: {str(e)}")
#         return None















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
    
    # METHOD 1: Try Streamlit secrets (FOR STREAMLIT CLOUD)
    try:
        import streamlit as st
        if 'google_token' in st.secrets:
            print("🔍 Found Streamlit secrets")
            token_info = dict(st.secrets['google_token'])
            # Convert list to actual list (Streamlit stores as ConfigList)
            if 'scopes' in token_info:
                token_info['scopes'] = list(token_info['scopes'])
            creds = Credentials.from_authorized_user_info(token_info, SCOPES)
            print("✅ Loaded credentials from Streamlit secrets")
            
            # Refresh if expired
            if creds.expired and creds.refresh_token:
                print("🔄 Refreshing expired token...")
                creds.refresh(Request())
                print("✅ Token refreshed")
            
            return build('calendar', 'v3', credentials=creds)
    except ImportError:
        print("ℹ️ Not in Streamlit environment")
    except KeyError:
        print("⚠️ No google_token in Streamlit secrets")
    except Exception as e:
        print(f"⚠️ Streamlit secrets error: {e}")
    
    # METHOD 2: Try environment variables (FOR RENDER/RAILWAY)
    if os.getenv('GOOGLE_TOKEN'):
        try:
            print("🔍 Found GOOGLE_TOKEN environment variable")
            token_data = json.loads(os.getenv('GOOGLE_TOKEN'))
            creds = Credentials.from_authorized_user_info(token_data, SCOPES)
            print("✅ Loaded credentials from environment")
            
            # Refresh if expired
            if creds.expired and creds.refresh_token:
                print("🔄 Refreshing expired token...")
                creds.refresh(Request())
                print("✅ Token refreshed")
            
            return build('calendar', 'v3', credentials=creds)
        except Exception as e:
            print(f"❌ Environment variable error: {e}")
    
    # METHOD 3: Try local file (FOR LOCAL DEVELOPMENT)
    if os.path.exists(TOKEN_PATH):
        try:
            print("🔍 Found local token file")
            creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)
            print("✅ Loaded credentials from file")
            
            # Refresh if expired
            if creds.expired and creds.refresh_token:
                print("🔄 Refreshing expired token...")
                creds.refresh(Request())
                print("✅ Token refreshed")
                # Save refreshed token
                with open(TOKEN_PATH, 'w') as token:
                    token.write(creds.to_json())
            
            return build('calendar', 'v3', credentials=creds)
        except Exception as e:
            print(f"❌ Local file error: {e}")
    
    # METHOD 4: Local OAuth (ONLY FOR LOCAL DEVELOPMENT)
    if os.path.exists(CREDENTIALS_PATH):
        print("\n🔐 Starting local OAuth flow...")
        print("⚠️ This only works on your laptop!")
        flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_PATH, SCOPES)
        creds = flow.run_local_server(port=0)
        print("✅ Authentication successful!")
        
        # Save token
        with open(TOKEN_PATH, 'w') as token:
            token.write(creds.to_json())
            print(f"✅ Token saved to {TOKEN_PATH}")
        
        return build('calendar', 'v3', credentials=creds)
    
    # If we get here, nothing worked
    raise Exception(
        "❌ Could not authenticate!\n"
        "For Streamlit Cloud: Add google_token to secrets\n"
        "For other platforms: Set GOOGLE_TOKEN environment variable\n"
        "For local: Run 'python scheduler/google_calendar.py' first"
    )


def get_upcoming_events(max_results=10):
    """Fetch upcoming events from Google Calendar."""
    try:
        service = get_calendar_service()
        now = datetime.datetime.utcnow().isoformat() + 'Z'

        events_result = service.events().list(
            calendarId='primary',
            timeMin=now,
            maxResults=max_results,
            singleEvents=True,
            orderBy='startTime'
        ).execute()

        return events_result.get('items', [])

    except HttpError as e:
        print(f"❌ Error fetching events: {e}")
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

            if start and end:
                start_dt = datetime.datetime.fromisoformat(start.replace('Z', '+00:00'))
                end_dt = datetime.datetime.fromisoformat(end.replace('Z', '+00:00'))

                events_list.append({
                    'summary': event.get('summary', 'Untitled'),
                    'start': start_dt.astimezone(LOCAL_TZ),
                    'end': end_dt.astimezone(LOCAL_TZ),
                    'id': event.get('id')
                })

        return events_list

    except HttpError as e:
        print(f"❌ Error fetching events: {e}")
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

    except HttpError as e:
        print(f"❌ Error fetching busy times: {e}")
        return []


def create_event(summary, start_datetime, end_datetime, description="", attendees=None):
    """Create a calendar event with correct time (timezone-safe)."""
    try:
        service = get_calendar_service()

        event = {
            "summary": summary,
            "description": description,
            "start": {
                "dateTime": start_datetime.isoformat(),
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
        print(f"❌ Error creating event: {e}")
        return None


def test_calendar_connection():
    """Simple diagnostic test."""
    print("\n=== Testing Google Calendar API ===")

    try:
        svc = get_calendar_service()
        print("✅ Authenticated successfully!")

        events = get_upcoming_events(3)
        print(f"📅 Fetched {len(events)} upcoming events.")

        now = datetime.datetime.now(LOCAL_TZ)
        busy = get_busy_times(now, now + datetime.timedelta(days=7))
        print(f"🔒 Busy slots this week: {len(busy)}")

        print("\n✅ All tests passed!")

    except Exception as e:
        print(f"\n❌ Test failed: {e}")


if __name__ == "__main__":
    test_calendar_connection()