import re
from datetime import datetime, timedelta
import pytz

LOCAL_TZ = pytz.timezone('Asia/Kolkata')

def parse_meeting_request(user_input, current_date=None):
    """
    Parse natural language meeting request using rule-based extraction.
    
    Args:
        user_input: User's natural language request (string)
        current_date: Reference date for parsing (datetime object)
    
    Returns:
        Dictionary with parsed fields or None if parsing fails
    """
    
    if current_date is None:
        current_date = datetime.now(LOCAL_TZ)
    
    user_input = user_input.lower()
    
    # Initialize result
    result = {
        'title': 'Meeting',
        'date': None,
        'time': None,
        'duration_minutes': 30,  # default
        'attendees': [],
        'description': ''
    }
    
    # Extract title/purpose
    title_patterns = [
        r'(?:schedule|book|set up|create|plan)\s+(?:a\s+)?(.+?)\s+(?:for|on|at|tomorrow|next|today)',
        r'(.+?)\s+meeting',
        r'meeting\s+(?:with|for)\s+(.+?)(?:\s+on|\s+at|\s+tomorrow|\s+next|$)'
    ]
    
    for pattern in title_patterns:
        match = re.search(pattern, user_input)
        if match:
            result['title'] = match.group(1).strip().title()
            break
    
    # Extract duration
    duration_patterns = [
        (r'(\d+)\s*(?:hour|hr|h)(?:s)?', 60),
        (r'(\d+)\s*(?:minute|min|m)(?:s)?', 1),
        (r'(\d+\.?\d*)\s*(?:hour|hr|h)(?:s)?', 60)
    ]
    
    for pattern, multiplier in duration_patterns:
        match = re.search(pattern, user_input)
        if match:
            result['duration_minutes'] = int(float(match.group(1)) * multiplier)
            break
    
    # Extract emails
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    emails = re.findall(email_pattern, user_input)
    result['attendees'] = emails
    
    # Extract date
    result['date'] = extract_date(user_input, current_date)
    
    # Extract time
    result['time'] = extract_time(user_input)
    
    # Validate
    if not result['date'] or not result['time']:
        return None
    
    return result


def extract_date(text, reference_date):
    """Extract date from text."""
    
    # Today
    if 'today' in text:
        return reference_date.strftime('%Y-%m-%d')
    
    # Tomorrow
    if 'tomorrow' in text:
        tomorrow = reference_date + timedelta(days=1)
        return tomorrow.strftime('%Y-%m-%d')
    
    # Day after tomorrow
    if 'day after tomorrow' in text or 'overmorrow' in text:
        day_after = reference_date + timedelta(days=2)
        return day_after.strftime('%Y-%m-%d')
    
    # Next [weekday]
    weekdays = {
        'monday': 0, 'mon': 0,
        'tuesday': 1, 'tue': 1, 'tues': 1,
        'wednesday': 2, 'wed': 2,
        'thursday': 3, 'thu': 3, 'thur': 3, 'thurs': 3,
        'friday': 4, 'fri': 4,
        'saturday': 5, 'sat': 5,
        'sunday': 6, 'sun': 6
    }
    
    for day_name, day_num in weekdays.items():
        if f'next {day_name}' in text or f'on {day_name}' in text:
            days_ahead = day_num - reference_date.weekday()
            if days_ahead <= 0:  # Target day already passed this week
                days_ahead += 7
            target_date = reference_date + timedelta(days=days_ahead)
            return target_date.strftime('%Y-%m-%d')
    
    # Specific date format: YYYY-MM-DD or DD-MM-YYYY or DD/MM/YYYY
    date_patterns = [
        r'(\d{4})-(\d{2})-(\d{2})',  # YYYY-MM-DD
        r'(\d{2})-(\d{2})-(\d{4})',  # DD-MM-YYYY
        r'(\d{2})/(\d{2})/(\d{4})',  # DD/MM/YYYY
    ]
    
    for pattern in date_patterns:
        match = re.search(pattern, text)
        if match:
            try:
                if len(match.group(1)) == 4:  # YYYY-MM-DD
                    return f"{match.group(1)}-{match.group(2)}-{match.group(3)}"
                else:  # DD-MM-YYYY or DD/MM/YYYY
                    day, month, year = match.group(1), match.group(2), match.group(3)
                    return f"{year}-{month}-{day}"
            except:
                pass
    
    # Default to tomorrow if no date found
    return (reference_date + timedelta(days=1)).strftime('%Y-%m-%d')


def extract_time(text):
    """Extract time from text."""
    
    # 24-hour format: 14:30, 09:00
    match = re.search(r'(\d{1,2}):(\d{2})', text)
    if match:
        hour = int(match.group(1))
        minute = int(match.group(2))
        return f"{hour:02d}:{minute:02d}"
    
    # 12-hour format: 3pm, 3:30pm, 3 pm
    match = re.search(r'(\d{1,2})(?::(\d{2}))?\s*(am|pm)', text)
    if match:
        hour = int(match.group(1))
        minute = int(match.group(2)) if match.group(2) else 0
        period = match.group(3)
        
        if period == 'pm' and hour != 12:
            hour += 12
        elif period == 'am' and hour == 12:
            hour = 0
        
        return f"{hour:02d}:{minute:02d}"
    
    # Time of day keywords
    time_keywords = {
        'morning': '10:00',
        'noon': '12:00',
        'afternoon': '14:00',
        'evening': '17:00',
        'night': '19:00'
    }
    
    for keyword, time in time_keywords.items():
        if keyword in text:
            return time
    
    # Default to 10:00 AM
    return '10:00'


def parse_datetime_from_parsed_data(parsed_data):
    """
    Convert parsed date and time strings into datetime object.
    
    Args:
        parsed_data: Dictionary from parse_meeting_request()
    
    Returns:
        datetime object (timezone-aware)
    """
    
    date_str = parsed_data['date']
    time_str = parsed_data['time']
    
    # Combine date and time
    dt_str = f"{date_str} {time_str}"
    dt = datetime.strptime(dt_str, '%Y-%m-%d %H:%M')
    
    # Make timezone-aware
    dt_aware = LOCAL_TZ.localize(dt)
    
    return dt_aware


def test_parser():
    """Test the parser with various inputs."""
    
    test_cases = [
        "Schedule a meeting tomorrow at 3pm for 30 minutes",
        "Book 1 hour team sync next Monday morning",
        "Set up a call with John at john@example.com on Friday afternoon",
        "Meeting with dev team on 2025-12-01 at 14:30 for 45 minutes",
        "Quick 15 min standup tomorrow morning",
        "Schedule team meeting today at 2:30pm",
        "Book conference room next Tuesday at 10am for 2 hours"
    ]
    
    print("Testing Rule-Based Parser (No API needed!)")
    print("=" * 60)
    
    for i, test_input in enumerate(test_cases, 1):
        print(f"\nTest {i}: {test_input}")
        print("-" * 60)
        
        result = parse_meeting_request(test_input)
        
        if result:
            print("✓ Parsed successfully:")
            print(f"  Title: {result['title']}")
            print(f"  Date: {result['date']}")
            print(f"  Time: {result['time']}")
            print(f"  Duration: {result['duration_minutes']} minutes")
            print(f"  Attendees: {result['attendees']}")
            
            # Test datetime conversion
            try:
                dt = parse_datetime_from_parsed_data(result)
                print(f"  DateTime: {dt.strftime('%Y-%m-%d %H:%M %Z')}")
            except Exception as e:
                print(f"  ✗ DateTime conversion failed: {e}")
        else:
            print("✗ Parsing failed")
    
    print("\n" + "=" * 60)


if __name__ == "__main__":
    test_parser()
