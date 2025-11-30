import streamlit as st
from google.oauth2 import service_account
from googleapiclient.discovery import build
import datetime
import pytz
import json

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scheduler.gpt_parser import parse_meeting_request
from scheduler.scheduler_logic import suggest_best_slot, format_slot_for_display
from scheduler.google_calendar import get_calendar_service, create_event, get_upcoming_events
from groq import Groq

st.set_page_config(page_title="AI Meeting Scheduler", page_icon="📅", layout="wide")

LOCAL_TZ = pytz.timezone('Asia/Kolkata')

# No login needed! Service account handles authentication automatically
st.title("📅 AI Meeting Scheduler")
st.info("✅ Connected to Skandana's Calendar")

# Test connection
if get_calendar_service():
    st.success("🎉 Calendar connection successful!")
else:
    st.error("❌ Could not connect to calendar. Check your secrets.")
    st.stop()

# Rest of your app code continues here...