# from datetime import datetime, timedelta
# import pytz
# try:
#     from scheduler.google_calendar import get_busy_times, get_events_in_range
# except ModuleNotFoundError:
#     from google_calendar import get_busy_times, get_events_in_range

# LOCAL_TZ = pytz.timezone('Asia/Kolkata')

# def find_available_slots(date, duration_minutes, working_hours=(9, 18), max_slots=3):
#     """
#     Find available time slots on a given date.
    
#     Args:
#         date: datetime.date object
#         duration_minutes: Required duration in minutes
#         working_hours: Tuple of (start_hour, end_hour) in 24h format
#         max_slots: Maximum number of slots to return
    
#     Returns:
#         List of available slots: [{'start': datetime, 'end': datetime}, ...]
#     """
    
#     # Define search window for the day
#     start_of_day = LOCAL_TZ.localize(
#         datetime.combine(date, datetime.min.time().replace(hour=working_hours[0]))
#     )
#     end_of_day = LOCAL_TZ.localize(
#         datetime.combine(date, datetime.min.time().replace(hour=working_hours[1]))
#     )
    
#     # Get busy times from calendar
#     busy_slots = get_busy_times(start_of_day, end_of_day)
    
#     # Generate all possible slots (every 30 minutes)
#     available_slots = []
#     current_time = start_of_day
#     slot_duration = timedelta(minutes=duration_minutes)
    
#     while current_time + slot_duration <= end_of_day:
#         slot_end = current_time + slot_duration
        
#         # Check if this slot conflicts with any busy time
#         is_available = True
#         for busy in busy_slots:
#             # Check for overlap
#             if not (slot_end <= busy['start'] or current_time >= busy['end']):
#                 is_available = False
#                 break
        
#         if is_available:
#             available_slots.append({
#                 'start': current_time,
#                 'end': slot_end
#             })
            
#             if len(available_slots) >= max_slots:
#                 break
        
#         # Move to next 30-min slot
#         current_time += timedelta(minutes=30)
    
#     return available_slots


# def suggest_best_slot(parsed_data, current_datetime=None):
#     """
#     Suggest the best available slot based on parsed meeting request.
    
#     Args:
#         parsed_data: Output from parse_meeting_request()
#         current_datetime: Current time (for testing)
    
#     Returns:
#         Dictionary with suggested slot or error message
#     """
    
#     if current_datetime is None:
#         current_datetime = datetime.now(LOCAL_TZ)
    
#     try:
#         # Parse requested date
#         requested_date = datetime.strptime(parsed_data['date'], '%Y-%m-%d').date()
#         requested_time = datetime.strptime(parsed_data['time'], '%H:%M').time()
#         duration = parsed_data['duration_minutes']
        
#         # Create full datetime
#         requested_datetime = LOCAL_TZ.localize(
#             datetime.combine(requested_date, requested_time)
#         )
        
#         # Check if requested time is in the past
#         if requested_datetime < current_datetime:
#             return {
#                 'success': False,
#                 'message': 'The requested time is in the past. Please choose a future time.'
#             }
        
#         # Check if requested slot is available
#         end_datetime = requested_datetime + timedelta(minutes=duration)
#         day_start = LOCAL_TZ.localize(datetime.combine(requested_date, datetime.min.time()))
#         day_end = LOCAL_TZ.localize(datetime.combine(requested_date, datetime.max.time()))
        
#         # Get all events in the requested time range
#         events_in_range = get_events_in_range(requested_datetime, end_datetime)
        
#         if not events_in_range:
#             # No conflict - requested slot is available!
#             return {
#                 'success': True,
#                 'slot': {
#                     'start': requested_datetime,
#                     'end': end_datetime
#                 },
#                 'message': 'Your requested time slot is available!'
#             }
#         else:
#             # There's a conflict - get the conflicting event details
#             conflicting_event = events_in_range[0]
            
#             # Find alternative slots
#             alternatives = find_available_slots(
#                 requested_date,
#                 duration,
#                 max_slots=3
#             )
            
#             if alternatives:
#                 return {
#                     'success': True,
#                     'slot': alternatives[0],  # Best alternative
#                     'alternatives': alternatives,  # All alternatives including best
#                     'conflict': {
#                         'summary': conflicting_event.get('summary', 'Untitled Event'),
#                         'start': conflicting_event['start'],
#                         'end': conflicting_event['end']
#                     },
#                     'message': 'Your requested time conflicts with an existing event. Here are available alternatives:'
#                 }
#             else:
#                 return {
#                     'success': False,
#                     'conflict': {
#                         'summary': conflicting_event.get('summary', 'Untitled Event'),
#                         'start': conflicting_event['start'],
#                         'end': conflicting_event['end']
#                     },
#                     'message': f'No available slots found on {requested_date}. Your calendar is fully booked.'
#                 }
    
#     except Exception as e:
#         return {
#             'success': False,
#             'message': f'Error finding available slot: {str(e)}'
#         }


# def format_slot_for_display(slot):
#     """Format a time slot for user-friendly display."""
#     start = slot['start']
#     end = slot['end']
    
#     # Format: "Thu, Nov 28 at 3:00 PM - 3:30 PM"
#     return {
#         'date': start.strftime('%a, %b %d'),
#         'time_range': f"{start.strftime('%I:%M %p')} - {end.strftime('%I:%M %p')}",
#         'full_display': f"{start.strftime('%a, %b %d at %I:%M %p')} - {end.strftime('%I:%M %p')}"
#     }


# def test_scheduling_logic():
#     """Test the scheduling logic."""
#     print("Testing Scheduling Logic")
#     print("=" * 60)
    
#     # Test case: Find slots for tomorrow
#     tomorrow = datetime.now(LOCAL_TZ).date() + timedelta(days=1)
    
#     print(f"\n1. Finding available 30-minute slots for {tomorrow}")
#     print("-" * 60)
    
#     slots = find_available_slots(tomorrow, 30, max_slots=5)
    
#     if slots:
#         print(f"✓ Found {len(slots)} available slots:")
#         for i, slot in enumerate(slots, 1):
#             formatted = format_slot_for_display(slot)
#             print(f"  {i}. {formatted['full_display']}")
#     else:
#         print("⚠ No available slots found (calendar might be fully booked)")
    
#     print("\n" + "=" * 60)
#     print("✓ Scheduling logic test completed!")


# if __name__ == "__main__":
#     test_scheduling_logic()

























from datetime import datetime, timedelta
import pytz
try:
    from scheduler.google_calendar import get_busy_times, get_events_in_range
except ModuleNotFoundError:
    from google_calendar import get_busy_times, get_events_in_range

LOCAL_TZ = pytz.timezone('Asia/Kolkata')

def find_available_slots(date, duration_minutes, working_hours=(9, 18), max_slots=3, current_datetime=None):
    """
    Find available time slots on a given date.
    
    Args:
        date: datetime.date object
        duration_minutes: Required duration in minutes
        working_hours: Tuple of (start_hour, end_hour) in 24h format
        max_slots: Maximum number of slots to return
        current_datetime: Current datetime (to filter out past times)
    
    Returns:
        List of available slots: [{'start': datetime, 'end': datetime}, ...]
    """
    
    if current_datetime is None:
        current_datetime = datetime.now(LOCAL_TZ)
    
    # Define search window for the day
    start_of_day = LOCAL_TZ.localize(
        datetime.combine(date, datetime.min.time().replace(hour=working_hours[0]))
    )
    end_of_day = LOCAL_TZ.localize(
        datetime.combine(date, datetime.min.time().replace(hour=working_hours[1]))
    )
    
    # Get busy times from calendar
    busy_slots = get_busy_times(start_of_day, end_of_day)
    
    # Generate all possible slots (every 30 minutes)
    available_slots = []
    current_time = start_of_day
    slot_duration = timedelta(minutes=duration_minutes)
    
    while current_time + slot_duration <= end_of_day:
        slot_end = current_time + slot_duration
        
        # **FIX: Skip if slot is in the past**
        if current_time < current_datetime:
            current_time += timedelta(minutes=30)
            continue
        
        # Check if this slot conflicts with any busy time
        is_available = True
        for busy in busy_slots:
            # Check for overlap
            if not (slot_end <= busy['start'] or current_time >= busy['end']):
                is_available = False
                break
        
        if is_available:
            available_slots.append({
                'start': current_time,
                'end': slot_end
            })
            
            if len(available_slots) >= max_slots:
                break
        
        # Move to next 30-min slot
        current_time += timedelta(minutes=30)
    
    return available_slots


def suggest_best_slot(parsed_data, current_datetime=None):
    """
    Suggest the best available slot based on parsed meeting request.
    
    Args:
        parsed_data: Output from parse_meeting_request()
        current_datetime: Current time (for testing)
    
    Returns:
        Dictionary with suggested slot or error message
    """
    
    if current_datetime is None:
        current_datetime = datetime.now(LOCAL_TZ)
    
    try:
        # Parse requested date
        requested_date = datetime.strptime(parsed_data['date'], '%Y-%m-%d').date()
        requested_time = datetime.strptime(parsed_data['time'], '%H:%M').time()
        duration = parsed_data['duration_minutes']
        
        # Create full datetime
        requested_datetime = LOCAL_TZ.localize(
            datetime.combine(requested_date, requested_time)
        )
        
        # Check if requested time is in the past
        if requested_datetime < current_datetime:
            return {
                'success': False,
                'message': 'The requested time is in the past. Please choose a future time.'
            }
        
        # Check if requested slot is available
        end_datetime = requested_datetime + timedelta(minutes=duration)
        
        # Get all events in the requested time range
        events_in_range = get_events_in_range(requested_datetime, end_datetime)
        
        if not events_in_range:
            # No conflict - requested slot is available!
            return {
                'success': True,
                'slot': {
                    'start': requested_datetime,
                    'end': end_datetime
                },
                'message': 'Your requested time slot is available!'
            }
        else:
            # There's a conflict - get the conflicting event details
            conflicting_event = events_in_range[0]
            
            # **FIX: Find alternative slots, passing current_datetime**
            alternatives = find_available_slots(
                requested_date,
                duration,
                max_slots=3,
                current_datetime=current_datetime  # Pass current time!
            )
            
            # **FIX: If no slots today, try tomorrow**
            if not alternatives:
                tomorrow = requested_date + timedelta(days=1)
                alternatives = find_available_slots(
                    tomorrow,
                    duration,
                    max_slots=3,
                    current_datetime=current_datetime
                )
            
            if alternatives:
                return {
                    'success': True,
                    'slot': alternatives[0],  # Best alternative
                    'alternatives': alternatives,  # All alternatives including best
                    'conflict': {
                        'summary': conflicting_event.get('summary', 'Untitled Event'),
                        'start': conflicting_event['start'],
                        'end': conflicting_event['end']
                    },
                    'message': 'Your requested time conflicts with an existing event. Here are available alternatives:'
                }
            else:
                return {
                    'success': False,
                    'conflict': {
                        'summary': conflicting_event.get('summary', 'Untitled Event'),
                        'start': conflicting_event['start'],
                        'end': conflicting_event['end']
                    },
                    'message': f'No available slots found on {requested_date} or the next day. Your calendar is fully booked.'
                }
    
    except Exception as e:
        return {
            'success': False,
            'message': f'Error finding available slot: {str(e)}'
        }


def format_slot_for_display(slot):
    """Format a time slot for user-friendly display."""
    start = slot['start']
    end = slot['end']
    
    # Format: "Thu, Nov 28 at 3:00 PM - 3:30 PM"
    return {
        'date': start.strftime('%a, %b %d'),
        'time_range': f"{start.strftime('%I:%M %p')} - {end.strftime('%I:%M %p')}",
        'full_display': f"{start.strftime('%a, %b %d at %I:%M %p')} - {end.strftime('%I:%M %p')}"
    }


def test_scheduling_logic():
    """Test the scheduling logic."""
    print("Testing Scheduling Logic")
    print("=" * 60)
    
    # Test case: Find slots for tomorrow
    tomorrow = datetime.now(LOCAL_TZ).date() + timedelta(days=1)
    
    print(f"\n1. Finding available 30-minute slots for {tomorrow}")
    print("-" * 60)
    
    slots = find_available_slots(tomorrow, 30, max_slots=5)
    
    if slots:
        print(f"✓ Found {len(slots)} available slots:")
        for i, slot in enumerate(slots, 1):
            formatted = format_slot_for_display(slot)
            print(f"  {i}. {formatted['full_display']}")
    else:
        print("⚠ No available slots found (calendar might be fully booked)")
    
    print("\n" + "=" * 60)
    print("✓ Scheduling logic test completed!")


if __name__ == "__main__":
    test_scheduling_logic()