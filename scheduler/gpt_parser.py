import os
import json
import re
from datetime import datetime, timedelta
import pytz
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(api_key=os.getenv('GROQ_API_KEY'))

LOCAL_TZ = pytz.timezone('Asia/Kolkata')

def parse_meeting_request(user_input, current_date=None):
    """Parse using Groq AI (FREE & FAST)"""
    
    if current_date is None:
        current_date = datetime.now(LOCAL_TZ)
    
    prompt = f"""You are a meeting scheduling assistant. Parse this request and return ONLY valid JSON.

Current date: {current_date.strftime('%Y-%m-%d %H:%M')} ({current_date.strftime('%A')})

Extract these fields:
- title: Meeting title/purpose
- date: YYYY-MM-DD format
- time: HH:MM format (24-hour)
- duration_minutes: integer (default 30)
- attendees: array of emails (empty if none)
- description: string

Rules:
- "tomorrow" = {(current_date + timedelta(days=1)).strftime('%Y-%m-%d')}
- "morning" = 10:00, "afternoon" = 14:00, "evening" = 17:00
- No time = 10:00, No duration = 30

User: "{user_input}"

Return ONLY JSON:"""

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",  # Free, powerful model
            messages=[{"role": "user", "content": prompt}],
            temperature=0.1,
            max_tokens=300
        )
        
        content = response.choices[0].message.content.strip()
        content = re.sub(r'```json\s*|\s*```', '', content).strip()
        
        parsed_data = json.loads(content)
        print("GPT PARSED:", parsed_data)

        
        # Validate
        required = ['title', 'date', 'time', 'duration_minutes']
        for field in required:
            if field not in parsed_data:
                return None
        
        datetime.strptime(parsed_data['date'], '%Y-%m-%d')
        datetime.strptime(parsed_data['time'], '%H:%M')
        
        if 'attendees' not in parsed_data:
            parsed_data['attendees'] = []
        if 'description' not in parsed_data:
            parsed_data['description'] = ''
        
        return parsed_data
    
    except Exception as e:
        print(f"❌ Error: {e}")
        return None


def parse_datetime_from_parsed_data(parsed_data):
    date_str = parsed_data['date']
    time_str = parsed_data['time']
    dt = datetime.strptime(f"{date_str} {time_str}", '%Y-%m-%d %H:%M')
    return LOCAL_TZ.localize(dt)


def test_parser():

    tests = [
        "Schedule meeting tomorrow at 3pm for 30 minutes",
        "Book 1 hour team sync next Monday morning",
        "Quick standup tomorrow morning"
    ]
    
    print("Testing Groq AI Parser (FREE)")
    print("=" * 70)
    
    for i, test in enumerate(tests, 1):
        print(f"\nTest {i}: {test}")
        print("-" * 70)
        result = parse_meeting_request(test)
        if result:
            print("✓ Success!")
            print(f"  Title: {result['title']}")
            print(f"  Date: {result['date']}")
            print(f"  Time: {result['time']}")
        else:
            print("✗ Failed")
    
    print("\n" + "=" * 70)

if __name__ == "__main__":
    if not os.getenv('GROQ_API_KEY'):
        print("❌ Add GROQ_API_KEY to .env")
    else:
        test_parser()








