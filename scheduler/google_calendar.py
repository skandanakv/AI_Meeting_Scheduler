import datetime
import pytz
import streamlit as st
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

LOCAL_TZ = pytz.timezone("Asia/Kolkata")


def load_credentials():
    """Load OAuth credentials entirely from Streamlit Secrets."""
    try:
        client_id = st.secrets["GOOGLE_CLIENT_ID"]
        client_secret = st.secrets["GOOGLE_CLIENT_SECRET"]
        redirect_uri = st.secrets["GOOGLE_REDIRECT_URI"]
        scopes = st.secrets["SCOPES"].split(", ")
    except KeyError as e:
        raise KeyError(f"Missing required Google OAuth secret: {e}")

    # Load stored user token (if user logged in before)
    if "user_token" in st.session_state:
        token_data = st.session_state["user_token"]
        creds = Credentials.from_authorized_user_info(token_data, scopes)

        # Refresh if expired
        if creds.expired and creds.refresh_token:
            creds.refresh(Request())
        return creds

    # If token missing → user must login
    return None


def get_login_url():
    """Generate Google OAuth login URL."""
    from google_auth_oauthlib.flow import Flow

    client_id = st.secrets["GOOGLE_CLIENT_ID"]
    client_secret = st.secrets["GOOGLE_CLIENT_SECRET"]
    redirect_uri = st.secrets["GOOGLE_REDIRECT_URI"]
    scopes = st.secrets["SCOPES"].split(", ")

    flow = Flow.from_client_config(
        {
            "web": {
                "client_id": client_id,
                "project_id": "streamlit-app",
                "auth_uri": st.secrets["GOOGLE_AUTH_URI"],
                "token_uri": st.secrets["GOOGLE_TOKEN_URI"],
                "client_secret": client_secret,
                "redirect_uris": [redirect_uri],
            }
        },
        scopes=scopes,
    )

    flow.redirect_uri = redirect_uri

    auth_url, _ = flow.authorization_url(
        access_type="offline",
        include_granted_scopes="true",
        prompt="consent"
    )

    return auth_url


def exchange_code_for_tokens(auth_code):
    """Convert Google OAuth ?code= into a usable token."""
    from google_auth_oauthlib.flow import Flow

    client_id = st.secrets["GOOGLE_CLIENT_ID"]
    client_secret = st.secrets["GOOGLE_CLIENT_SECRET"]
    redirect_uri = st.secrets["GOOGLE_REDIRECT_URI"]
    scopes = st.secrets["SCOPES"].split(", ")

    flow = Flow.from_client_config(
        {
            "web": {
                "client_id": client_id,
                "project_id": "streamlit-app",
                "auth_uri": st.secrets["GOOGLE_AUTH_URI"],
                "token_uri": st.secrets["GOOGLE_TOKEN_URI"],
                "client_secret": client_secret,
                "redirect_uris": [redirect_uri],
            }
        },
        scopes=scopes,
    )

    flow.redirect_uri = redirect_uri
    flow.fetch_token(code=auth_code)

    creds = flow.credentials

    # Save token in session
    st.session_state["user_token"] = {
        "token": creds.token,
        "refresh_token": creds.refresh_token,
        "token_uri": creds.token_uri,
        "client_id": creds.client_id,
        "client_secret": creds.client_secret,
        "scopes": creds.scopes,
    }

    return creds


def get_calendar_service():
    """Return authorized Google Calendar client."""
    creds = load_credentials()

    if creds is None:
        st.error("🔐 Google Calendar not connected. Please log in.")
        return None

    try:
        return build("calendar", "v3", credentials=creds)
    except Exception as e:
        st.error(f"Google Calendar error: {e}")
        return None


# ---------------------------- API FUNCTIONS ----------------------------

def get_upcoming_events(max_results=10):
    service = get_calendar_service()
    if not service:
        return []

    now = datetime.datetime.utcnow().isoformat() + "Z"
    events = (
        service.events()
        .list(
            calendarId="primary",
            timeMin=now,
            maxResults=max_results,
            singleEvents=True,
            orderBy="startTime",
        )
        .execute()
        .get("items", [])
    )
    return events


def get_events_in_range(start_datetime, end_datetime):
    service = get_calendar_service()
    if not service:
        return []

    time_min = start_datetime.astimezone(pytz.UTC).isoformat()
    time_max = end_datetime.astimezone(pytz.UTC).isoformat()

    try:
        events = (
            service.events()
            .list(
                calendarId="primary",
                timeMin=time_min,
                timeMax=time_max,
                singleEvents=True,
                orderBy="startTime",
            )
            .execute()
            .get("items", [])
        )

        formatted = []
        for e in events:
            s = datetime.datetime.fromisoformat(
                e["start"]["dateTime"].replace("Z", "+00:00")
            ).astimezone(LOCAL_TZ)
            t = datetime.datetime.fromisoformat(
                e["end"]["dateTime"].replace("Z", "+00:00")
            ).astimezone(LOCAL_TZ)
            formatted.append({"summary": e["summary"], "start": s, "end": t})

        return formatted

    except HttpError:
        return []


def get_busy_times(start_datetime, end_datetime):
    service = get_calendar_service()
    if not service:
        return []

    time_min = start_datetime.astimezone(pytz.UTC).isoformat()
    time_max = end_datetime.astimezone(pytz.UTC).isoformat()

    body = {"timeMin": time_min, "timeMax": time_max, "items": [{"id": "primary"}]}

    try:
        busy = service.freebusy().query(body=body).execute()
        slots = busy["calendars"]["primary"]["busy"]

        results = []
        for slot in slots:
            s = datetime.datetime.fromisoformat(slot["start"].replace("Z", "+00:00")).astimezone(LOCAL_TZ)
            t = datetime.datetime.fromisoformat(slot["end"].replace("Z", "+00:00")).astimezone(LOCAL_TZ)
            results.append({"start": s, "end": t})

        return results

    except HttpError:
        return []


def create_event(summary, start_datetime, end_datetime, description="", attendees=None):
    service = get_calendar_service()
    if not service:
        return None

    body = {
        "summary": summary,
        "description": description,
        "start": {"dateTime": start_datetime.isoformat()},
        "end": {"dateTime": end_datetime.isoformat()},
    }

    if attendees:
        body["attendees"] = [{"email": x} for x in attendees]

    try:
        return service.events().insert(calendarId="primary", body=body).execute()
    except HttpError:
        return None
