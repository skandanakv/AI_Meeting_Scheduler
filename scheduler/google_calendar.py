import datetime
import pytz
import requests
import streamlit as st
from urllib.parse import urlencode

# Timezone
LOCAL_TZ = pytz.timezone("Asia/Kolkata")

# Read from Streamlit Secrets
CLIENT_ID = st.secrets["GOOGLE_CLIENT_ID"]
CLIENT_SECRET = st.secrets["GOOGLE_CLIENT_SECRET"]
REDIRECT_URI = st.secrets["GOOGLE_REDIRECT_URI"]
AUTH_URI = st.secrets["GOOGLE_AUTH_URI"]
TOKEN_URI = st.secrets["GOOGLE_TOKEN_URI"]
SCOPES = st.secrets["SCOPES"]


# ---------------------------------------------------------
# 1. GENERATE AUTH URL
# ---------------------------------------------------------
def get_google_auth_url():
    params = {
        "client_id": CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
        "response_type": "code",
        "scope": " ".join(SCOPES),
        "access_type": "offline",
        "prompt": "consent"
    }
    return AUTH_URI + "?" + urlencode(params)


# ---------------------------------------------------------
# 2. EXCHANGE AUTH CODE FOR TOKEN
# ---------------------------------------------------------
def exchange_code_for_token(auth_code):
    data = {
        "code": auth_code,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "redirect_uri": REDIRECT_URI,
        "grant_type": "authorization_code"
    }
    response = requests.post(TOKEN_URI, data=data)

    if response.status_code != 200:
        print("Token Error:", response.text)
        return None

    return response.json()


# ---------------------------------------------------------
# 3. GET GOOGLE CALENDAR EVENTS
# ---------------------------------------------------------
def google_api_get(url, access_token, params=None):
    headers = {"Authorization": f"Bearer {access_token}"}
    r = requests.get(url, headers=headers, params=params)
    if r.status_code != 200:
        print("API Error:", r.text)
    return r.json()


# UPCOMING EVENTS
def get_upcoming_events(access_token, max_results=10):
    url = "https://www.googleapis.com/calendar/v3/calendars/primary/events"
    params = {
        "orderBy": "startTime",
        "singleEvents": True,
        "timeMin": datetime.datetime.utcnow().isoformat() + "Z",
        "maxResults": max_results
    }
    data = google_api_get(url, access_token, params)
    return data.get("items", [])


# EVENTS FOR PARTICULAR DATE
def get_events_for_date(access_token, date_obj):
    start = datetime.datetime.combine(date_obj, datetime.time.min).astimezone(pytz.UTC).isoformat()
    end = datetime.datetime.combine(date_obj, datetime.time.max).astimezone(pytz.UTC).isoformat()

    url = "https://www.googleapis.com/calendar/v3/calendars/primary/events"
    params = {
        "orderBy": "startTime",
        "singleEvents": True,
        "timeMin": start,
        "timeMax": end
    }
    data = google_api_get(url, access_token, params)
    return data.get("items", [])


# ---------------------------------------------------------
# 4. CREATE EVENT
# ---------------------------------------------------------
def create_event(access_token, summary, start_datetime, end_datetime, description=""):
    url = "https://www.googleapis.com/calendar/v3/calendars/primary/events"

    event = {
        "summary": summary,
        "description": description,
        "start": {"dateTime": start_datetime.isoformat()},
        "end": {"dateTime": end_datetime.isoformat()}
    }

    headers = {"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"}
    r = requests.post(url, headers=headers, json=event)

    if r.status_code not in (200, 201):
        print("Create Event Error:", r.text)
        return None

    return r.json()
