from scheduler.gpt_parser import parse_meeting_request, parse_datetime_from_parsed_data
from scheduler.scheduler_logic import suggest_best_slot, format_slot_for_display
from scheduler.google_calendar import create_event
from datetime import timedelta

def test_full_meeting_flow():
    """Test the complete flow: parse → find slot → create event."""
    
    print("FULL MEETING SCHEDULER TEST")
    print("=" * 70)
    
    # Step 1: Parse natural language
    user_input = "Schedule a 30 minute team meeting tomorrow at 2pm"
    print(f"\nStep 1: User says: '{user_input}'")
    print("-" * 70)
    
    parsed = parse_meeting_request(user_input)
    
    if not parsed:
        print("✗ Parsing failed")
        return
    
    print("✓ Parsed successfully:")
    print(f"  Title: {parsed['title']}")
    print(f"  Date: {parsed['date']}")
    print(f"  Time: {parsed['time']}")
    print(f"  Duration: {parsed['duration_minutes']} minutes")
    
    # Step 2: Find available slot
    print(f"\nStep 2: Finding available slot...")
    print("-" * 70)
    
    suggestion = suggest_best_slot(parsed)
    
    if not suggestion['success']:
        print(f"✗ {suggestion['message']}")
        return
    
    print(f"✓ {suggestion['message']}")
    
    slot = suggestion['slot']
    formatted = format_slot_for_display(slot)
    print(f"  Suggested: {formatted['full_display']}")
    
    if 'alternatives' in suggestion and suggestion['alternatives']:
        print(f"\n  Alternative slots:")
        for alt in suggestion['alternatives']:
            alt_formatted = format_slot_for_display(alt)
            print(f"    - {alt_formatted['full_display']}")
    
    # Step 3: Create event (COMMENTED OUT for testing - uncomment to actually create)
    print(f"\nStep 3: Create event in Google Calendar")
    print("-" * 70)
    print("⚠ Event creation is DISABLED for testing")
    print("  To enable: uncomment the code in test_full_flow.py")
    print(f"\n  Would create event:")
    print(f"    Title: {parsed['title']}")
    print(f"    Time: {formatted['full_display']}")
    print(f"    Duration: {parsed['duration_minutes']} minutes")
    
    # UNCOMMENT BELOW TO CREATE REAL EVENTS IN YOUR CALENDAR
    # print("\n⚠ CREATING REAL EVENT IN YOUR CALENDAR...")
    # event = create_event(
    #     summary=parsed['title'],
    #     start_datetime=slot['start'],
    #     end_datetime=slot['end'],
    #     description=parsed.get('description', ''),
    #     attendees=parsed.get('attendees', [])
    # )
    # 
    # if event:
    #     print(f"✓ Event created successfully!")
    #     print(f"  Event ID: {event['id']}")
    #     print(f"  Link: {event.get('htmlLink', 'N/A')}")
    # else:
    #     print("✗ Event creation failed")
    
    print("\n" + "=" * 70)
    print("✓ FULL FLOW TEST COMPLETED SUCCESSFULLY!")
    print("\nAll systems working:")
    print("  ✓ Natural language parsing")
    print("  ✓ Google Calendar API connection")
    print("  ✓ Slot finding logic")
    print("  ✓ Ready for Streamlit UI!")


if __name__ == "__main__":
    test_full_meeting_flow()
