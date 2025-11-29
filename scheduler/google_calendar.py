import streamlit as st
import requests
import datetime
import pytz
from googleapiclient.discovery import build

# Timezone
LOCAL_TZ = pytz.timezone("Asia/Kolkata")

SCOPES = [
    "https://www.googleapis.com/auth/calendar.events",
    "https://www.googleapis.com/auth/calendar.readonly",
]


# ------------------------------------------------------
# 1️⃣ GOOGLE LOGIN FLOW (STREAMLIT CLOUD COMPATIBLE)
# ------------------------------------------------------
def ensure_google_login():
    """
    Shows Login button if user is not authenticated.
    Saves Google OAuth token in session_state.
    """

    # Already authenticated
    if "google_token" in st.session_state:
        return True

    # Build Google OAuth URL
    auth_url = (
        f"{st.secrets['GOOGLE_AUTH_URI']}?"
        f"client_id={st.secrets['GOOGLE_CLIENT_ID']}&"
        f"redirect_uri={st.secrets['GOOGLE_REDIRECT_URI']}&"
        f"response_type=code&"
        f"scope={' '.join(SCOPES)}&"
        f"access_type=offline&"
        f"prompt=consent"
    )

    st.markdown(
        f"""
        <a href="{auth_url}" target="_self">
            <button style="
                padding: 10px 22px;
                font-size: 16px;
                border-radius: 8px;
                border:none;
                background:#4b6cb7;
                color:white;
                cursor:pointer;">
                🔐 Login with Google
            </button>
        </a>
        """,
        unsafe_allow_html=True,
    )

    # If redirected back with ?code=...
    params = st.experimental_get_query_params()
    if "code" in params:
        code = params["code"][0]

        # Exchange code for access token
        token_payload = {
            "code": code,
            "client_id": st.secrets["GOOGLE_CLIENT_ID"],
            "client_secret": st.secrets["GOOGLE_CLIENT_SECRET"],
            "redirect_uri": st.secrets["GOOGLE_REDIRECT_URI"],
            "grant_type": "authorization_code",
        }

        response = requests.post(st.secrets["GOOGLE_TOKEN_URI"], data=token_payload)
        token_data = response.json()

        if "access_token" in token_data:
            st.session_state["google_token"] = token_data
            st.success("Google Calendar Connected! 🎉")
            st.experimental_rerun()
        else:
            st.error("Google login failed. Please try again.")

    return False


# ------------------------------------------------------
# 2️⃣ BUILD CALENDAR SERVICE FROM TOKEN
# ------------------------------------------------------
def get_calendar_service():
    """Returns authenticated Google Calendar API service."""
    if "google_token" not in st.session_state:
        return None

    token = st.session_state["google_token"]
    access_token = token["access_token"]

    session = requests.Session()
    session.headers.update({"Authorization": f"Bearer {access_token}"})

    # Build Google Calendar service
    return build(
        "calendar",
        "v3",
        developerKey=None,
        requestBuilder=lambda *args, **kwargs: None,
        http=session,
    )


# ------------------------------------------------------
# 3️⃣ FETCH UPCOMING EVENTS
# ------------------------------------------------------
def get_upcoming_events(max_results=10):
    service = get_calendar_service()
    if not service:
        return None  # Not logged in

    now = datetime.datetime.utcnow().isoformat() + "Z"

    events_result = service.events().list(
        calendarId="primary",
        timeMin=now,
        maxResults=max_results,
        singleEvents=True,
        orderBy="startTime",
    ).execute()

    return events_result.get("items", [])


# ------------------------------------------------------
# 4️⃣ FETCH EVENTS FOR SPECIFIC RANGE
# ------------------------------------------------------
def get_events_in_range(start, end):
    service = get_calendar_service()
    if not service:
        return None

    events_result = service.events().list(
        calendarId="primary",
        timeMin=start.astimezone(pytz.UTC).isoformat(),
        timeMax=end.astimezone(pytz.UTC).isoformat(),
        singleEvents=True,
        orderBy="startTime",
    ).execute()

    events = []
    for ev in events_result.get("items", []):
        s = ev["start"]["dateTime"]
        e = ev["end"]["dateTime"]
        s_dt = datetime.datetime.fromisoformat(s.replace("Z", "+00:00")).astimezone(LOCAL_TZ)
        e_dt = datetime.datetime.fromisoformat(e.replace("Z", "+00:00")).astimezone(LOCAL_TZ)

        events.append({"summary": ev.get("summary"), "start": s_dt, "end": e_dt})

    return events


# ------------------------------------------------------
# 5️⃣ CREATE EVENT
# ------------------------------------------------------
def create_event(summary, start_datetime, end_datetime, description="", attendees=None):
    service = get_calendar_service()
    if not service:
        return None

    event_body = {
        "summary": summary,
        "description": description,
        "start": {"dateTime": start_datetime.isoformat()},
        "end": {"dateTime": end_datetime.isoformat()},
    }

    if attendees:
        event_body["attendees"] = [{"email": a} for a in attendees]

    return (
        service.events()
        .insert(calendarId="primary", body=event_body)
        .execute()
    )
