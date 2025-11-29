# # # import os
# # # import json
# # # import re
# # # from datetime import datetime, timedelta
# # # import pytz
# # # from dotenv import load_dotenv
# # # from groq import Groq
# # # import streamlit as st


# # # load_dotenv()

# # # try:
# # #     # Try Streamlit Cloud secrets first
# # #     api_key = st.secrets.get("GROQ_API_KEY")
# # #     if not api_key:
# # #         raise ValueError("GROQ_API_KEY not found in secrets")
# # # except:
# # #     # Fall back to environment variables for local development
# # #     api_key = os.getenv('GROQ_API_KEY')
# # #     if not api_key:
# # #         raise ValueError("GROQ_API_KEY not found in environment")

# # # client = Groq(api_key=api_key)

# # # LOCAL_TZ = pytz.timezone('Asia/Kolkata')

# # # def parse_meeting_request(user_input, current_date=None):
# # #     """Parse using Groq AI (FREE & FAST)"""
    
# # #     if current_date is None:
# # #         current_date = datetime.now(LOCAL_TZ)
    
# # #     prompt = f"""You are a meeting scheduling assistant. Parse this request and return ONLY valid JSON.

# # # Current date: {current_date.strftime('%Y-%m-%d %H:%M')} ({current_date.strftime('%A')})

# # # Extract these fields:
# # # - title: Meeting title/purpose
# # # - date: YYYY-MM-DD format
# # # - time: HH:MM format (24-hour)
# # # - duration_minutes: integer (default 30)
# # # - attendees: array of emails (empty if none)
# # # - description: string

# # # Rules:
# # # - "tomorrow" = {(current_date + timedelta(days=1)).strftime('%Y-%m-%d')}
# # # - "morning" = 10:00, "afternoon" = 14:00, "evening" = 17:00
# # # - No time = 10:00, No duration = 30

# # # User: "{user_input}"

# # # Return ONLY JSON:"""

# # #     try:
# # #         response = client.chat.completions.create(
# # #             model="llama-3.3-70b-versatile",  # Free, powerful model
# # #             messages=[{"role": "user", "content": prompt}],
# # #             temperature=0.1,
# # #             max_tokens=300
# # #         )
        
# # #         content = response.choices[0].message.content.strip()
# # #         content = re.sub(r'```json\s*|\s*```', '', content).strip()
        
# # #         parsed_data = json.loads(content)
# # #         print("GPT PARSED:", parsed_data)

        
# # #         # Validate
# # #         required = ['title', 'date', 'time', 'duration_minutes']
# # #         for field in required:
# # #             if field not in parsed_data:
# # #                 return None
        
# # #         datetime.strptime(parsed_data['date'], '%Y-%m-%d')
# # #         datetime.strptime(parsed_data['time'], '%H:%M')
        
# # #         if 'attendees' not in parsed_data:
# # #             parsed_data['attendees'] = []
# # #         if 'description' not in parsed_data:
# # #             parsed_data['description'] = ''
        
# # #         return parsed_data
    
# # #     except Exception as e:
# # #         print(f"❌ Error: {e}")
# # #         return None


# # # def parse_datetime_from_parsed_data(parsed_data):
# # #     date_str = parsed_data['date']
# # #     time_str = parsed_data['time']
# # #     dt = datetime.strptime(f"{date_str} {time_str}", '%Y-%m-%d %H:%M')
# # #     return LOCAL_TZ.localize(dt)


# # # def test_parser():

# # #     tests = [
# # #         "Schedule meeting tomorrow at 3pm for 30 minutes",
# # #         "Book 1 hour team sync next Monday morning",
# # #         "Quick standup tomorrow morning"
# # #     ]
    
# # #     print("Testing Groq AI Parser (FREE)")
# # #     print("=" * 70)
    
# # #     for i, test in enumerate(tests, 1):
# # #         print(f"\nTest {i}: {test}")
# # #         print("-" * 70)
# # #         result = parse_meeting_request(test)
# # #         if result:
# # #             print("✓ Success!")
# # #             print(f"  Title: {result['title']}")
# # #             print(f"  Date: {result['date']}")
# # #             print(f"  Time: {result['time']}")
# # #         else:
# # #             print("✗ Failed")
    
# # #     print("\n" + "=" * 70)

# # # if __name__ == "__main__":
# # #     if not os.getenv('GROQ_API_KEY'):
# # #         print("❌ Add GROQ_API_KEY to .env")
# # #     else:
# # #         test_parser()








# # import os
# # import json
# # import re
# # from datetime import datetime, timedelta
# # import pytz
# # from dotenv import load_dotenv
# # from groq import Groq

# # load_dotenv()

# # LOCAL_TZ = pytz.timezone('Asia/Kolkata')

# # def get_groq_api_key():
# #     """Get Groq API key from Streamlit secrets or environment variables"""
# #     api_key = None
    
# #     # Try Streamlit Cloud secrets first
# #     try:
# #         import streamlit as st
# #         if hasattr(st, 'secrets'):
# #             api_key = st.secrets.get("GROQ_API_KEY")
# #             if api_key:
# #                 return api_key.strip()
# #     except Exception:
# #         pass
    
# #     # Fall back to environment variables for local development
# #     api_key = os.getenv('GROQ_API_KEY')
# #     if api_key:
# #         return api_key.strip()
    
# #     raise ValueError("GROQ_API_KEY not found in Streamlit secrets or environment variables")

# # # Initialize Groq client
# # api_key = get_groq_api_key()
# # client = Groq(api_key=api_key)

# # def parse_meeting_request(user_input, current_date=None):
# #     """Parse using Groq AI (FREE & FAST)"""
    
# #     if current_date is None:
# #         current_date = datetime.now(LOCAL_TZ)
    
# #     prompt = f"""You are a meeting scheduling assistant. Parse this request and return ONLY valid JSON.

# # Current date: {current_date.strftime('%Y-%m-%d %H:%M')} ({current_date.strftime('%A')})

# # Extract these fields:
# # - title: Meeting title/purpose
# # - date: YYYY-MM-DD format
# # - time: HH:MM format (24-hour)
# # - duration_minutes: integer (default 30)
# # - attendees: array of emails (empty if none)
# # - description: string

# # Rules:
# # - "tomorrow" = {(current_date + timedelta(days=1)).strftime('%Y-%m-%d')}
# # - "morning" = 10:00, "afternoon" = 14:00, "evening" = 17:00
# # - No time = 10:00, No duration = 30

# # User: "{user_input}"

# # Return ONLY JSON:"""

# #     try:
# #         response = client.chat.completions.create(
# #             model="llama-3.3-70b-versatile",
# #             messages=[{"role": "user", "content": prompt}],
# #             temperature=0.1,
# #             max_tokens=300
# #         )
        
# #         content = response.choices[0].message.content.strip()
# #         content = re.sub(r'```json\s*|\s*```', '', content).strip()
        
# #         parsed_data = json.loads(content)
# #         print("GPT PARSED:", parsed_data)
        
# #         # Validate required fields
# #         required = ['title', 'date', 'time', 'duration_minutes']
# #         for field in required:
# #             if field not in parsed_data:
# #                 return None
        
# #         # Validate date/time formats
# #         datetime.strptime(parsed_data['date'], '%Y-%m-%d')
# #         datetime.strptime(parsed_data['time'], '%H:%M')
        
# #         # Add optional fields if missing
# #         if 'attendees' not in parsed_data:
# #             parsed_data['attendees'] = []
# #         if 'description' not in parsed_data:
# #             parsed_data['description'] = ''
        
# #         return parsed_data
    
# #     except Exception as e:
# #         print(f"❌ Error: {e}")
# #         return None


# # def parse_datetime_from_parsed_data(parsed_data):
# #     """Convert parsed data to timezone-aware datetime"""
# #     date_str = parsed_data['date']
# #     time_str = parsed_data['time']
# #     dt = datetime.strptime(f"{date_str} {time_str}", '%Y-%m-%d %H:%M')
# #     return LOCAL_TZ.localize(dt)


# # def test_parser():
# #     """Test the parser with sample inputs"""
# #     tests = [
# #         "Schedule meeting tomorrow at 3pm for 30 minutes",
# #         "Book 1 hour team sync next Monday morning",
# #         "Quick standup tomorrow morning"
# #     ]
    
# #     print("Testing Groq AI Parser (FREE)")
# #     print("=" * 70)
    
# #     for i, test in enumerate(tests, 1):
# #         print(f"\nTest {i}: {test}")
# #         print("-" * 70)
# #         result = parse_meeting_request(test)
# #         if result:
# #             print("✓ Success!")
# #             print(f"  Title: {result['title']}")
# #             print(f"  Date: {result['date']}")
# #             print(f"  Time: {result['time']}")
# #         else:
# #             print("✗ Failed")
    
# #     print("\n" + "=" * 70)


# # if __name__ == "__main__":
# #     try:
# #         api_key = get_groq_api_key()
# #         print("✓ GROQ_API_KEY found")
# #         test_parser()
# #     except ValueError as e:
# #         print(f"❌ {e}")






















# import os
# import json
# import re
# from datetime import datetime, timedelta
# import pytz
# from dotenv import load_dotenv
# from groq import Groq

# load_dotenv()

# LOCAL_TZ = pytz.timezone('Asia/Kolkata')

# # Global client variable (initialized lazily)
# _client = None

# def get_groq_client():
#     """Get or create Groq client (lazy initialization)"""
#     global _client
    
#     if _client is not None:
#         return _client
    
#     api_key = None
    
#     # Try Streamlit Cloud secrets first
#     try:
#         import streamlit as st
#         if hasattr(st, 'secrets') and "GROQ_API_KEY" in st.secrets:
#             api_key = st.secrets["GROQ_API_KEY"]
#     except Exception:
#         pass
    
#     # Fall back to environment variables for local development
#     if not api_key:
#         api_key = os.getenv('GROQ_API_KEY')
    
#     if not api_key:
#         raise ValueError("❌ GROQ_API_KEY not found")
    
#     # Remove any quotes that might be in the key
#     api_key = api_key.strip().strip('"').strip("'")
    
#     if not api_key.startswith('gsk_'):
#         raise ValueError(f"❌ Invalid GROQ_API_KEY format")
    
#     _client = Groq(api_key=api_key)
#     return _client


# def parse_meeting_request(user_input, current_date=None):
#     """Parse using Groq AI (FREE & FAST)"""
    
#     if current_date is None:
#         current_date = datetime.now(LOCAL_TZ)
    
#     prompt = f"""You are a meeting scheduling assistant. Parse this request and return ONLY valid JSON.

# Current date: {current_date.strftime('%Y-%m-%d %H:%M')} ({current_date.strftime('%A')})

# Extract these fields:
# - title: Meeting title/purpose
# - date: YYYY-MM-DD format
# - time: HH:MM format (24-hour)
# - duration_minutes: integer (default 30)
# - attendees: array of emails (empty if none)
# - description: string

# Rules:
# - "tomorrow" = {(current_date + timedelta(days=1)).strftime('%Y-%m-%d')}
# - "morning" = 10:00, "afternoon" = 14:00, "evening" = 17:00
# - No time = 10:00, No duration = 30

# User: "{user_input}"

# Return ONLY JSON:"""

#     try:
#         client = get_groq_client()  # ✅ Get client lazily (not at module level)
        
#         response = client.chat.completions.create(
#             model="llama-3.3-70b-versatile",
#             messages=[{"role": "user", "content": prompt}],
#             temperature=0.1,
#             max_tokens=300
#         )
        
#         content = response.choices[0].message.content.strip()
#         content = re.sub(r'```json\s*|\s*```', '', content).strip()
        
#         parsed_data = json.loads(content)
#         print("GPT PARSED:", parsed_data)
        
#         # Validate required fields
#         required = ['title', 'date', 'time', 'duration_minutes']
#         for field in required:
#             if field not in parsed_data:
#                 return None
        
#         # Validate date/time formats
#         datetime.strptime(parsed_data['date'], '%Y-%m-%d')
#         datetime.strptime(parsed_data['time'], '%H:%M')
        
#         # Add optional fields if missing
#         if 'attendees' not in parsed_data:
#             parsed_data['attendees'] = []
#         if 'description' not in parsed_data:
#             parsed_data['description'] = ''
        
#         return parsed_data
    
#     except Exception as e:
#         print(f"❌ Error: {e}")
#         return None


# def parse_datetime_from_parsed_data(parsed_data):
#     """Convert parsed data to timezone-aware datetime"""
#     date_str = parsed_data['date']
#     time_str = parsed_data['time']
#     dt = datetime.strptime(f"{date_str} {time_str}", '%Y-%m-%d %H:%M')
#     return LOCAL_TZ.localize(dt)


# def test_parser():
#     """Test the parser with sample inputs"""
#     tests = [
#         "Schedule meeting tomorrow at 3pm for 30 minutes",
#         "Book 1 hour team sync next Monday morning",
#         "Quick standup tomorrow morning"
#     ]
    
#     print("Testing Groq AI Parser")
#     print("=" * 70)
    
#     for i, test in enumerate(tests, 1):
#         print(f"\nTest {i}: {test}")
#         print("-" * 70)
#         result = parse_meeting_request(test)
#         if result:
#             print("✓ Success!")
#             print(f"  Title: {result['title']}")
#             print(f"  Date: {result['date']}")
#             print(f"  Time: {result['time']}")
#         else:
#             print("✗ Failed")
    
#     print("\n" + "=" * 70)


# if __name__ == "__main__":
#     try:
#         get_groq_client()
#         print("✓ GROQ_API_KEY found and valid")
#         test_parser()
#     except ValueError as e:
#         print(f"❌ {e}")














import os
import json
import re
from datetime import datetime, timedelta
import pytz
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

LOCAL_TZ = pytz.timezone("Asia/Kolkata")

# Cached client instance
_client = None


# --------------------------------------------------
#  SAFE — Groq only initializes inside this function
# --------------------------------------------------
def get_groq_client():
    global _client
    if _client is not None:
        return _client

    api_key = None

    # Try Streamlit secrets first
    try:
        import streamlit as st
        if "GROQ_API_KEY" in st.secrets:
            api_key = st.secrets["GROQ_API_KEY"]
    except:
        pass

    # If not found, use environment (.env)
    if not api_key:
        api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        raise ValueError("❌ GROQ_API_KEY missing — add to Streamlit Secrets or .env")

    api_key = api_key.strip().replace('"', "").replace("'", "")

    if not api_key.startswith("gsk_"):
        raise ValueError("❌ Invalid GROQ_API_KEY format")

    # IMPORTANT: Client is created ONLY here (safe for Streamlit)
    _client = Groq(api_key=api_key)
    return _client


# --------------------------------------------------
#  PARSER
# --------------------------------------------------
def parse_meeting_request(user_input, current_date=None):
    if current_date is None:
        current_date = datetime.now(LOCAL_TZ)

    prompt = f"""
You are an AI meeting scheduling assistant. Parse the user's request and return ONLY JSON.

Current date: {current_date.strftime("%Y-%m-%d %H:%M")} ({current_date.strftime("%A")})

Extract and return:
- title: string
- date: YYYY-MM-DD
- time: HH:MM (24-hour)
- duration_minutes: integer (default 30)
- attendees: list of emails
- description: string

Interpretation rules:
- "tomorrow" = {(current_date + timedelta(days=1)).strftime("%Y-%m-%d")}
- morning = 10:00
- afternoon = 14:00
- evening = 17:00
- No time → 10:00
- No duration → 30 minutes

User request:
"{user_input}"

Return ONLY JSON. No extra text.
"""

    try:
        client = get_groq_client()

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=300,
            temperature=0.1
        )

        content = response.choices[0].message.content.strip()

        # Remove JSON fences
        content = re.sub(r"```json|```", "", content).strip()

        parsed = json.loads(content)

        # Validate required fields
        for field in ["title", "date", "time", "duration_minutes"]:
            if field not in parsed:
                return None

        # Validate date & time format
        datetime.strptime(parsed["date"], "%Y-%m-%d")
        datetime.strptime(parsed["time"], "%H:%M")

        # Add default empty fields
        parsed.setdefault("attendees", [])
        parsed.setdefault("description", "")

        return parsed

    except Exception as e:
        print(f"[PARSER ERROR] {e}")
        return None


# --------------------------------------------------
# Convert parsed fields → datetime object
# --------------------------------------------------
def parse_datetime_from_parsed_data(parsed_data):
    dt_str = f"{parsed_data['date']} {parsed_data['time']}"
    dt = datetime.strptime(dt_str, "%Y-%m-%d %H:%M")
    return LOCAL_TZ.localize(dt)

