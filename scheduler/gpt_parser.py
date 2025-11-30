import os
import json
from datetime import datetime, timedelta
import pytz
from groq import Groq

LOCAL_TZ = pytz.timezone("Asia/Kolkata")

# Cached client instance
_client = None


def get_groq_client():
    """Initialize Groq client (cached, safe for Streamlit)"""
    global _client
    if _client is not None:
        return _client

    api_key = None

    # Try Streamlit secrets first
    try:
        import streamlit as st
        if "GROQ_API_KEY" in st.secrets:
            api_key = st.secrets["GROQ_API_KEY"]
            print("✅ Using Groq API key from Streamlit secrets")
    except:
        pass

    # Fallback to environment variable
    if not api_key:
        api_key = os.getenv("GROQ_API_KEY")
        if api_key:
            print("✅ Using Groq API key from environment")

    if not api_key:
        raise ValueError("❌ GROQ_API_KEY not found!")

    # Clean the key
    api_key = api_key.strip().replace('"', '').replace("'", '')

    # Create client WITHOUT proxies parameter (this was the bug!)
    _client = Groq(api_key=api_key)
    return _client


def parse_meeting_request(user_input, current_date=None):
    """Parse natural language meeting request using Groq LLM"""
    if current_date is None:
        current_date = datetime.now(LOCAL_TZ)

    tomorrow = (current_date + timedelta(days=1)).strftime("%Y-%m-%d")
    
    system_prompt = f"""You are a meeting scheduler AI. Extract meeting details and return ONLY valid JSON.

Current date/time: {current_date.strftime("%Y-%m-%d %H:%M")} ({current_date.strftime("%A")})
Tomorrow's date: {tomorrow}

Rules:
1. "today" → use {current_date.strftime("%Y-%m-%d")}
2. "tomorrow" → use {tomorrow}
3. "4pm" or "4 pm" → "16:00"
4. No time given → "10:00"
5. No duration → 30 minutes
6. "morning" → 10:00, "afternoon" → 14:00, "evening" → 17:00

Return ONLY this JSON (no markdown, no extra text):
{{
  "title": "Meeting Title",
  "date": "YYYY-MM-DD",
  "time": "HH:MM",
  "duration_minutes": 30,
  "attendees": [],
  "description": ""
}}

User request: "{user_input}"
"""

    try:
        client = get_groq_client()

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": system_prompt}],
            max_tokens=300,
            temperature=0.1
        )

        content = response.choices[0].message.content.strip()
        print(f"🤖 Groq response: {content}")

        # Remove markdown fences if present
        if content.startswith("```"):
            lines = content.split('\n')
            content = '\n'.join([line for line in lines if not line.startswith("```")])
            content = content.replace("json", "").strip()

        # Parse JSON
        parsed = json.loads(content)

        # Validate required fields
        required = ["title", "date", "time", "duration_minutes"]
        for field in required:
            if field not in parsed:
                print(f"❌ Missing required field: {field}")
                return None

        # Validate formats
        datetime.strptime(parsed["date"], "%Y-%m-%d")
        datetime.strptime(parsed["time"], "%H:%M")

        # Set defaults
        parsed.setdefault("attendees", [])
        parsed.setdefault("description", "")

        print(f"✅ Successfully parsed: {parsed}")
        return parsed

    except json.JSONDecodeError as e:
        print(f"[PARSER ERROR] JSON decode failed: {e}")
        print(f"Raw response: {content}")
        return None
    except Exception as e:
        print(f"[PARSER ERROR] {e}")
        return None


def parse_datetime_from_parsed_data(parsed_data):
    """Convert parsed data to datetime object"""
    dt_str = f"{parsed_data['date']} {parsed_data['time']}"
    dt = datetime.strptime(dt_str, "%Y-%m-%d %H:%M")
    return LOCAL_TZ.localize(dt)
