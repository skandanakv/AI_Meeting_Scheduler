# # # # # # # # # # app.py — Clean, fixed version
# # # # # # # # # import streamlit as st
# # # # # # # # # from datetime import datetime, timedelta, date
# # # # # # # # # import pytz
# # # # # # # # # import calendar as cal_module

# # # # # # # # # # Your project modules (must exist)
# # # # # # # # # from scheduler.gpt_parser import parse_meeting_request, parse_datetime_from_parsed_data
# # # # # # # # # from scheduler.scheduler_logic import suggest_best_slot, format_slot_for_display
# # # # # # # # # from scheduler.google_calendar import create_event, get_upcoming_events

# # # # # # # # # # -------------------------
# # # # # # # # # # Page + session init
# # # # # # # # # # -------------------------
# # # # # # # # # st.set_page_config(page_title="AI Meeting Scheduler", page_icon="📅", layout="wide")

# # # # # # # # # LOCAL_TZ = pytz.timezone("Asia/Kolkata")

# # # # # # # # # if "messages" not in st.session_state:
# # # # # # # # #     st.session_state.messages = []
# # # # # # # # # if "pending_slot" not in st.session_state:
# # # # # # # # #     st.session_state.pending_slot = None
# # # # # # # # # if "pending_parsed_data" not in st.session_state:
# # # # # # # # #     st.session_state.pending_parsed_data = None
# # # # # # # # # if "current_suggestion" not in st.session_state:
# # # # # # # # #     st.session_state.current_suggestion = None
# # # # # # # # # if "selected_alternative" not in st.session_state:
# # # # # # # # #     st.session_state.selected_alternative = None
# # # # # # # # # if "event_created" not in st.session_state:
# # # # # # # # #     st.session_state.event_created = False
# # # # # # # # # # internal token used to append a single confirmation message after rerun
# # # # # # # # # if "_pending_confirm_msg" not in st.session_state:
# # # # # # # # #     st.session_state._pending_confirm_msg = None

# # # # # # # # # # UI CSS
# # # # # # # # # st.markdown(
# # # # # # # # #     """
# # # # # # # # # <style>
# # # # # # # # #     .main-header { font-size: 2.2rem; font-weight: 700; color: #1f77b4; text-align: center; margin-bottom: 6px; }
# # # # # # # # #     .sub-header { font-size: 1.05rem; color: #666; text-align: center; margin-bottom: 14px; }
# # # # # # # # #     .calendar-grid { display: grid; grid-template-columns: repeat(7, 1fr); gap: 4px; margin: 8px 0; }
# # # # # # # # #     .calendar-day { aspect-ratio: 1; display:flex; align-items:center; justify-content:center; background:#f0f2f6; border-radius:6px; font-size:0.85rem; font-weight:500; }
# # # # # # # # #     .calendar-header { font-weight:700; background:#1f77b4; color:white; }
# # # # # # # # #     .calendar-today { background:#4CAF50; color:white; font-weight:700; }
# # # # # # # # # </style>
# # # # # # # # # """,
# # # # # # # # #     unsafe_allow_html=True,
# # # # # # # # # )

# # # # # # # # # # -------------------------
# # # # # # # # # # Sidebar (calendar + upcoming)
# # # # # # # # # # -------------------------
# # # # # # # # # with st.sidebar:
# # # # # # # # #     st.markdown("### 📅 Meeting Scheduler")
# # # # # # # # #     st.markdown("---")

# # # # # # # # #     # calendar overview
# # # # # # # # #     today = date.today()
# # # # # # # # #     if "current_month" not in st.session_state:
# # # # # # # # #         st.session_state.current_month = today.month
# # # # # # # # #     if "current_year" not in st.session_state:
# # # # # # # # #         st.session_state.current_year = today.year

# # # # # # # # #     col1, col2, col3 = st.columns([1, 2, 1])
# # # # # # # # #     with col1:
# # # # # # # # #         if st.button("◀", key="prev_month"):
# # # # # # # # #             if st.session_state.current_month == 1:
# # # # # # # # #                 st.session_state.current_month = 12
# # # # # # # # #                 st.session_state.current_year -= 1
# # # # # # # # #             else:
# # # # # # # # #                 st.session_state.current_month -= 1
# # # # # # # # #     with col2:
# # # # # # # # #         month_name = cal_module.month_name[st.session_state.current_month]
# # # # # # # # #         st.markdown(f"**{month_name} {st.session_state.current_year}**")
# # # # # # # # #     with col3:
# # # # # # # # #         if st.button("▶", key="next_month"):
# # # # # # # # #             if st.session_state.current_month == 12:
# # # # # # # # #                 st.session_state.current_month = 1
# # # # # # # # #                 st.session_state.current_year += 1
# # # # # # # # #             else:
# # # # # # # # #                 st.session_state.current_month += 1

# # # # # # # # #     cal = cal_module.monthcalendar(st.session_state.current_year, st.session_state.current_month)
# # # # # # # # #     calendar_html = '<div class="calendar-grid">'
# # # # # # # # #     for day in ['Mo','Tu','We','Th','Fr','Sa','Su']:
# # # # # # # # #         calendar_html += f'<div class="calendar-day calendar-header">{day}</div>'
# # # # # # # # #     for week in cal:
# # # # # # # # #         for d in week:
# # # # # # # # #             if d == 0:
# # # # # # # # #                 calendar_html += '<div class="calendar-day"></div>'
# # # # # # # # #             else:
# # # # # # # # #                 is_today = (d == today.day and st.session_state.current_month == today.month and st.session_state.current_year == today.year)
# # # # # # # # #                 css = "calendar-today" if is_today else ""
# # # # # # # # #                 calendar_html += f'<div class="calendar-day {css}">{d}</div>'
# # # # # # # # #     calendar_html += '</div>'
# # # # # # # # #     st.markdown(calendar_html, unsafe_allow_html=True)

# # # # # # # # #     st.markdown("---")
# # # # # # # # #     st.markdown("### 📋 Upcoming Events")
# # # # # # # # #     try:
# # # # # # # # #         events = get_upcoming_events(5)
# # # # # # # # #         if events:
# # # # # # # # #             for ev in events:
# # # # # # # # #                 start = ev['start'].get('dateTime', ev['start'].get('date'))
# # # # # # # # #                 st.markdown(f"**{ev.get('summary','Untitled')}**")
# # # # # # # # #                 st.caption(start)
# # # # # # # # #                 st.markdown("---")
# # # # # # # # #         else:
# # # # # # # # #             st.info("No upcoming events")
# # # # # # # # #     except Exception:
# # # # # # # # #         st.warning("Could not load calendar events")

# # # # # # # # #     st.markdown("---")
# # # # # # # # #     st.markdown("### 💡 How to use")
# # # # # # # # #     st.markdown(
# # # # # # # # #         "- Type a natural request (e.g., 'Schedule meeting tomorrow at 3pm')\n"
# # # # # # # # #         "- If conflict — click an alternate slot\n"
# # # # # # # # #         "- Confirm to create the event"
# # # # # # # # #     )
# # # # # # # # #     if st.button("🗑️ Clear chat", use_container_width=True):
# # # # # # # # #         st.session_state.messages = []
# # # # # # # # #         st.session_state.pending_slot = None
# # # # # # # # #         st.session_state.pending_parsed_data = None
# # # # # # # # #         st.session_state.current_suggestion = None
# # # # # # # # #         st.session_state.selected_alternative = None
# # # # # # # # #         st.session_state._pending_confirm_msg = None
# # # # # # # # #         st.experimental_rerun()

# # # # # # # # # # -------------------------
# # # # # # # # # # Main content header
# # # # # # # # # # -------------------------
# # # # # # # # # st.markdown('<div class="main-header">🤖 AI Meeting Scheduler Agent</div>', unsafe_allow_html=True)
# # # # # # # # # st.markdown('<div class="sub-header">Schedule meetings using natural language</div>', unsafe_allow_html=True)

# # # # # # # # # # -------------------------
# # # # # # # # # # Render chat messages
# # # # # # # # # # -------------------------
# # # # # # # # # for msg in st.session_state.messages:
# # # # # # # # #     with st.chat_message(msg["role"]):
# # # # # # # # #         st.markdown(msg["content"])

# # # # # # # # # # -------------------------
# # # # # # # # # # Chat input -> parse -> suggest
# # # # # # # # # # -------------------------
# # # # # # # # # user_input = st.chat_input("Type your meeting request here... (e.g., 'Schedule meeting tomorrow at 3pm')")

# # # # # # # # # if user_input:
# # # # # # # # #     # append user message once
# # # # # # # # #     st.session_state.messages.append({"role":"user","content":user_input})
# # # # # # # # #     with st.chat_message("user"):
# # # # # # # # #         st.markdown(user_input)

# # # # # # # # #     # parse + suggest
# # # # # # # # #     with st.chat_message("assistant"):
# # # # # # # # #         with st.spinner("🔍 Analyzing your request..."):
# # # # # # # # #             parsed = parse_meeting_request(user_input)
# # # # # # # # #             if not parsed:
# # # # # # # # #                 err = "❌ Couldn't understand. Try: 'Schedule meeting tomorrow at 3pm for 30 minutes'"
# # # # # # # # #                 st.markdown(err)
# # # # # # # # #                 st.session_state.messages.append({"role":"assistant","content":err})
# # # # # # # # #             else:
# # # # # # # # #                 suggestion = suggest_best_slot(parsed)
# # # # # # # # #                 # store parsed & suggestion
# # # # # # # # #                 st.session_state.pending_parsed_data = parsed
# # # # # # # # #                 st.session_state.current_suggestion = suggestion

# # # # # # # # #                 if not suggestion.get("success"):
# # # # # # # # #                     err = f"❌ {suggestion.get('message','Unable to find slots')}"
# # # # # # # # #                     st.markdown(err)
# # # # # # # # #                     st.session_state.messages.append({"role":"assistant","content":err})
# # # # # # # # #                 else:
# # # # # # # # #                     # if conflict -> show alternatives list later, else set pending slot
# # # # # # # # #                     if suggestion.get("conflict"):
# # # # # # # # #                         conflict = suggestion["conflict"]
# # # # # # # # #                         response = f"""⚠️ **Event Conflict Detected!**

# # # # # # # # # 🚫 **Existing Event at Requested Time:**
# # # # # # # # # - **Event Name:** {conflict.get('summary','Untitled')}
# # # # # # # # # - **Time:** {conflict['start'].strftime('%a, %b %d at %I:%M %p')} - {conflict['end'].strftime('%I:%M %p')}

# # # # # # # # # ✅ **Available Alternative Slots:**
# # # # # # # # # - **Title:** {parsed.get('title')}
# # # # # # # # # - **Duration:** {parsed.get('duration_minutes')} minutes

# # # # # # # # # 👇 Click on any available time slot below.
# # # # # # # # # """
# # # # # # # # #                         st.markdown(response)
# # # # # # # # #                         st.session_state.messages.append({"role":"assistant","content":response})
# # # # # # # # #                         # ensure pending_slot cleared
# # # # # # # # #                         st.session_state.pending_slot = None
# # # # # # # # #                         st.session_state.selected_alternative = None
# # # # # # # # #                     else:
# # # # # # # # #                         # available
# # # # # # # # #                         slot = suggestion["slot"]
# # # # # # # # #                         st.session_state.pending_slot = slot
# # # # # # # # #                         formatted = format_slot_for_display(slot)
# # # # # # # # #                         response = f"""✅ **Found slot**

# # # # # # # # # 📅 **{parsed.get('title')}**
# # # # # # # # # - **When:** {formatted['full_display']}
# # # # # # # # # - **Duration:** {parsed.get('duration_minutes')} minutes

# # # # # # # # # Click 'Confirm & Create Event' to book.
# # # # # # # # # """
# # # # # # # # #                         st.markdown(response)
# # # # # # # # #                         st.session_state.messages.append({"role":"assistant","content":response})

# # # # # # # # # # -------------------------
# # # # # # # # # # If the user previously clicked an alternative slot, append confirm message once
# # # # # # # # # # -------------------------
# # # # # # # # # if st.session_state._pending_confirm_msg:
# # # # # # # # #     # only append once then clear
# # # # # # # # #     msg = st.session_state._pending_confirm_msg
# # # # # # # # #     # avoid duplicate
# # # # # # # # #     last = st.session_state.messages[-1]["content"] if st.session_state.messages else None
# # # # # # # # #     if last != msg:
# # # # # # # # #         st.session_state.messages.append({"role":"assistant","content":msg})
# # # # # # # # #     st.session_state._pending_confirm_msg = None
# # # # # # # # #     # re-render messages area (Streamlit will rerun naturally)

# # # # # # # # # # -------------------------
# # # # # # # # # # Show alternative slot buttons (safe, no rerun inside handler)
# # # # # # # # # # -------------------------
# # # # # # # # # if st.session_state.current_suggestion and st.session_state.current_suggestion.get("alternatives"):
# # # # # # # # #     suggestion = st.session_state.current_suggestion
# # # # # # # # #     alts = suggestion.get("alternatives", [])
# # # # # # # # #     if alts:
# # # # # # # # #         st.markdown("---")
# # # # # # # # #         st.markdown("### 📅 Available Time Slots")
# # # # # # # # #         cols = st.columns(min(3, len(alts)))
# # # # # # # # #         for idx, slot in enumerate(alts):
# # # # # # # # #             formatted = format_slot_for_display(slot)
# # # # # # # # #             btn_key = f"alt_{idx}_{slot['start'].isoformat()}"
# # # # # # # # #             clicked = cols[idx % 3].button(f"📅 {formatted['date']}\n⏰ {formatted['time_range']}", key=btn_key, use_container_width=True)
# # # # # # # # #             if clicked:
# # # # # # # # #                 # store selection and a single confirm token (do NOT append message here)
# # # # # # # # #                 st.session_state.pending_slot = slot
# # # # # # # # #                 st.session_state.selected_alternative = idx
# # # # # # # # #                 st.session_state._pending_confirm_msg = f"✅ Selected: **{formatted['full_display']}**\n\nClick 'Confirm & Create Event' below to book this slot."

# # # # # # # # # # -------------------------
# # # # # # # # # # Confirmation block (create/cancel)
# # # # # # # # # # -------------------------
# # # # # # # # # if st.session_state.pending_slot:
# # # # # # # # #     st.markdown("---")
# # # # # # # # #     col1, col2, col3 = st.columns([1, 2, 1])
# # # # # # # # #     with col2:
# # # # # # # # #         confirm = st.button("✅ Confirm & Create Event", type="primary", use_container_width=True, key="confirm_create")
# # # # # # # # #         cancel = st.button("❌ Cancel", use_container_width=True, key="cancel_create")

# # # # # # # # #         if confirm:
# # # # # # # # #             with st.spinner("📅 Creating event..."):
# # # # # # # # #                 # prevent double-create
# # # # # # # # #                 if st.session_state.event_created:
# # # # # # # # #                     st.info("Event already created in this session.")
# # # # # # # # #                 else:
# # # # # # # # #                     try:
# # # # # # # # #                         slot = st.session_state.pending_slot
# # # # # # # # #                         parsed = st.session_state.pending_parsed_data
# # # # # # # # #                         created = create_event(
# # # # # # # # #                             summary=parsed.get("title","Meeting"),
# # # # # # # # #                             start_datetime=slot["start"],
# # # # # # # # #                             end_datetime=slot["end"],
# # # # # # # # #                             description=parsed.get("description","Created by AI Meeting Scheduler Agent"),
# # # # # # # # #                             attendees=parsed.get("attendees",[])
# # # # # # # # #                         )
# # # # # # # # #                         if created:
# # # # # # # # #                             formatted = format_slot_for_display(slot)
# # # # # # # # #                             success = f"""🎉 **Event Created Successfully!**

# # # # # # # # # 📅 **{parsed.get('title','Meeting')}**
# # # # # # # # # - **Time:** {formatted['full_display']}

# # # # # # # # # Event Link: {created.get('htmlLink','#')}
# # # # # # # # # """
# # # # # # # # #                             st.session_state.messages.append({"role":"assistant","content":success})
# # # # # # # # #                             # reset states
# # # # # # # # #                             st.session_state.pending_slot = None
# # # # # # # # #                             st.session_state.pending_parsed_data = None
# # # # # # # # #                             st.session_state.current_suggestion = None
# # # # # # # # #                             st.session_state.selected_alternative = None
# # # # # # # # #                             st.session_state.event_created = True
# # # # # # # # #                             st.success("✅ Event created successfully!")
# # # # # # # # #                             st.balloons()
# # # # # # # # #                             # rerun to refresh sidebar etc.
# # # # # # # # #                             st.experimental_rerun()
# # # # # # # # #                         else:
# # # # # # # # #                             err = "❌ Failed to create event. Try again."
# # # # # # # # #                             st.session_state.messages.append({"role":"assistant","content":err})
# # # # # # # # #                             st.error(err)
# # # # # # # # #                     except Exception as e:
# # # # # # # # #                         err = f"❌ Error creating event: {e}"
# # # # # # # # #                         st.session_state.messages.append({"role":"assistant","content":err})
# # # # # # # # #                         st.error(err)

# # # # # # # # #         if cancel:
# # # # # # # # #             # clear pending state safely (no rerun)
# # # # # # # # #             st.session_state.pending_slot = None
# # # # # # # # #             st.session_state.pending_parsed_data = None
# # # # # # # # #             st.session_state.current_suggestion = None
# # # # # # # # #             st.session_state.selected_alternative = None
# # # # # # # # #             st.session_state._pending_confirm_msg = None
# # # # # # # # #             cancel_msg = "❌ Meeting request cancelled. Feel free to make a new request!"
# # # # # # # # #             # avoid duplicate
# # # # # # # # #             last = st.session_state.messages[-1]["content"] if st.session_state.messages else None
# # # # # # # # #             if last != cancel_msg:
# # # # # # # # #                 st.session_state.messages.append({"role":"assistant","content":cancel_msg})

# # # # # # # # # # Footer
# # # # # # # # # st.markdown("---")
# # # # # # # # # st.markdown('<div style="text-align:center;color:#666;font-size:0.9rem;">Powered by Google Calendar API | Built with Streamlit</div>', unsafe_allow_html=True)






























# # # # import streamlit as st
# # # # from datetime import datetime, timedelta, date
# # # # import pytz
# # # # import calendar as cal_module

# # # # from scheduler.gpt_parser import parse_meeting_request, parse_datetime_from_parsed_data
# # # # from scheduler.scheduler_logic import suggest_best_slot, format_slot_for_display
# # # # from scheduler.google_calendar import create_event, get_upcoming_events

# # # # # -------------------------
# # # # # Page + session init
# # # # # -------------------------
# # # # st.set_page_config(page_title="AI Meeting Scheduler", page_icon="📅", layout="wide")

# # # # LOCAL_TZ = pytz.timezone("Asia/Kolkata")

# # # # if "messages" not in st.session_state:
# # # #     st.session_state.messages = []
# # # # if "pending_slot" not in st.session_state:
# # # #     st.session_state.pending_slot = None
# # # # if "pending_parsed_data" not in st.session_state:
# # # #     st.session_state.pending_parsed_data = None
# # # # if "current_suggestion" not in st.session_state:
# # # #     st.session_state.current_suggestion = None
# # # # if "selected_alternative" not in st.session_state:
# # # #     st.session_state.selected_alternative = None
# # # # if "event_created" not in st.session_state:
# # # #     st.session_state.event_created = False
# # # # if "_pending_confirm_msg" not in st.session_state:
# # # #     st.session_state._pending_confirm_msg = None

# # # # # -------------------------
# # # # # Helper function: Format datetime properly
# # # # # -------------------------
# # # # def format_event_time(event_time_str):
# # # #     """Convert ISO datetime string to readable format"""
# # # #     try:
# # # #         if 'T' in event_time_str:
# # # #             dt = datetime.fromisoformat(event_time_str.replace('Z', '+00:00'))
# # # #             dt_local = dt.astimezone(LOCAL_TZ)
# # # #             return dt_local.strftime('%a, %b %d at %I:%M %p')
# # # #         else:
# # # #             dt = datetime.strptime(event_time_str, '%Y-%m-%d')
# # # #             return dt.strftime('%a, %b %d (All day)')
# # # #     except:
# # # #         return event_time_str

# # # # def get_events_for_date(target_date):
# # # #     """Get all events for a specific date"""
# # # #     try:
# # # #         from scheduler.google_calendar import get_calendar_service
# # # #         import pytz
        
# # # #         service = get_calendar_service()
        
# # # #         start_of_day = LOCAL_TZ.localize(
# # # #             datetime.combine(target_date, datetime.min.time())
# # # #         )
# # # #         end_of_day = LOCAL_TZ.localize(
# # # #             datetime.combine(target_date, datetime.max.time())
# # # #         )
        
# # # #         time_min = start_of_day.astimezone(pytz.UTC).isoformat()
# # # #         time_max = end_of_day.astimezone(pytz.UTC).isoformat()
        
# # # #         events_result = service.events().list(
# # # #             calendarId='primary',
# # # #             timeMin=time_min,
# # # #             timeMax=time_max,
# # # #             singleEvents=True,
# # # #             orderBy='startTime'
# # # #         ).execute()
        
# # # #         events = events_result.get('items', [])
        
# # # #         formatted_events = []
# # # #         for event in events:
# # # #             start = event['start'].get('dateTime', event['start'].get('date'))
# # # #             end = event['end'].get('dateTime', event['end'].get('date'))
            
# # # #             if 'T' in start:
# # # #                 start_dt = datetime.fromisoformat(start.replace('Z', '+00:00')).astimezone(LOCAL_TZ)
# # # #                 end_dt = datetime.fromisoformat(end.replace('Z', '+00:00')).astimezone(LOCAL_TZ)
# # # #                 time_str = f"{start_dt.strftime('%I:%M %p')} - {end_dt.strftime('%I:%M %p')}"
# # # #             else:
# # # #                 time_str = "All day"
            
# # # #             formatted_events.append({
# # # #                 'summary': event.get('summary', 'Untitled'),
# # # #                 'time': time_str,
# # # #                 'description': event.get('description', '')
# # # #             })
        
# # # #         return formatted_events
# # # #     except Exception as e:
# # # #         return []

# # # # # -------------------------
# # # # # UI CSS
# # # # # -------------------------
# # # # st.markdown(
# # # #     """
# # # # <style>
# # # #     .main-header { font-size: 2.2rem; font-weight: 700; color: #1f77b4; text-align: center; margin-bottom: 6px; }
# # # #     .sub-header { font-size: 1.05rem; color: #666; text-align: center; margin-bottom: 14px; }
    
# # # #     /* Calendar Grid */
# # # #     .calendar-grid { 
# # # #         display: grid; 
# # # #         grid-template-columns: repeat(7, 1fr); 
# # # #         gap: 4px; 
# # # #         margin: 8px 0; 
# # # #     }
# # # #     .calendar-day { 
# # # #         aspect-ratio: 1; 
# # # #         display: flex; 
# # # #         align-items: center; 
# # # #         justify-content: center; 
# # # #         background: #f0f2f6; 
# # # #         border-radius: 6px; 
# # # #         font-size: 0.85rem; 
# # # #         font-weight: 500;
# # # #     }
# # # #     .calendar-header { 
# # # #         font-weight: 700; 
# # # #         background: #1f77b4; 
# # # #         color: white; 
# # # #     }
# # # #     .calendar-today { 
# # # #         background: #4CAF50; 
# # # #         color: white; 
# # # #         font-weight: 700; 
# # # #     }
# # # # </style>
# # # # """,
# # # #     unsafe_allow_html=True,
# # # # )

# # # # # -------------------------
# # # # # Sidebar (calendar + upcoming)
# # # # # -------------------------
# # # # with st.sidebar:
# # # #     st.markdown("### 📅 Meeting Scheduler")
# # # #     st.markdown("---")

# # # #     # Month navigation
# # # #     today = date.today()
# # # #     if "current_month" not in st.session_state:
# # # #         st.session_state.current_month = today.month
# # # #     if "current_year" not in st.session_state:
# # # #         st.session_state.current_year = today.year

# # # #     col1, col2, col3 = st.columns([1, 2, 1])
# # # #     with col1:
# # # #         if st.button("◀", key="prev_month"):
# # # #             if st.session_state.current_month == 1:
# # # #                 st.session_state.current_month = 12
# # # #                 st.session_state.current_year -= 1
# # # #             else:
# # # #                 st.session_state.current_month -= 1
# # # #             st.rerun()
# # # #     with col2:
# # # #         month_name = cal_module.month_name[st.session_state.current_month]
# # # #         st.markdown(f"**{month_name} {st.session_state.current_year}**")
# # # #     with col3:
# # # #         if st.button("▶", key="next_month"):
# # # #             if st.session_state.current_month == 12:
# # # #                 st.session_state.current_month = 1
# # # #                 st.session_state.current_year += 1
# # # #             else:
# # # #                 st.session_state.current_month += 1
# # # #             st.rerun()

# # # #     # Calendar display
# # # #     cal = cal_module.monthcalendar(st.session_state.current_year, st.session_state.current_month)
# # # #     calendar_html = '<div class="calendar-grid">'
    
# # # #     for day in ['Mo','Tu','We','Th','Fr','Sa','Su']:
# # # #         calendar_html += f'<div class="calendar-day calendar-header">{day}</div>'
    
# # # #     for week in cal:
# # # #         for d in week:
# # # #             if d == 0:
# # # #                 calendar_html += '<div class="calendar-day"></div>'
# # # #             else:
# # # #                 is_today = (d == today.day and 
# # # #                            st.session_state.current_month == today.month and 
# # # #                            st.session_state.current_year == today.year)
# # # #                 css = "calendar-today" if is_today else ""
# # # #                 calendar_html += f'<div class="calendar-day {css}">{d}</div>'
    
# # # #     calendar_html += '</div>'
# # # #     st.markdown(calendar_html, unsafe_allow_html=True)
    
# # # #     # Date selector - UPDATED SECTION
# # # #     st.markdown("---")
# # # #     st.markdown("**📅 View Events for Date:**")
    
# # # #     date_input = st.text_input(
# # # #         "Type date (DD/MM/YYYY)",
# # # #         placeholder="28/11/2025",
# # # #         key="manual_date_input",
# # # #         help="Enter date in DD/MM/YYYY format"
# # # #     )
    
# # # #     all_days = [d for week in cal for d in week if d != 0]
# # # #     # selected_day = st.selectbox(
# # # #     #     "Or select from current month",
# # # #     #     options=all_days,
# # # #     #     format_func=lambda x: f"{x:02d}/{st.session_state.current_month:02d}/{st.session_state.current_year}",
# # # #     #     key="day_selector"
# # # #     # )
    
# # # #     if st.button("📅 View Events", use_container_width=True, key="view_events_btn"):
# # # #         selected_date = None
        
# # # #         if date_input.strip():
# # # #             try:
# # # #                 parts = date_input.strip().split('/')
# # # #                 if len(parts) == 3:
# # # #                     day, month, year = int(parts[0]), int(parts[1]), int(parts[2])
# # # #                     selected_date = date(year, month, day)
# # # #             except:
# # # #                 st.error("❌ Invalid format! Use DD/MM/YYYY (e.g., 28/11/2025)")
        
# # # #         if not selected_date:
# # # #             selected_date = date(
# # # #                 st.session_state.current_year,
# # # #                 st.session_state.current_month,
# # # #                 selected_day
# # # #             )
        
# # # #         if selected_date:
# # # #             events = get_events_for_date(selected_date)
            
# # # #             st.markdown(f"**📆 {selected_date.strftime('%A, %B %d, %Y')}**")
# # # #             st.markdown("---")
            
# # # #             if events:
# # # #                 for event in events:
# # # #                     st.markdown(f"### 🕐 {event['time']}")
# # # #                     st.markdown(f"**{event['summary']}**")
# # # #                     if event.get('description'):
# # # #                         st.caption(event['description'])
# # # #                     st.markdown("---")
# # # #             else:
# # # #                 st.info(f"✨ No events on {selected_date.strftime('%B %d')}")

# # # #     st.markdown("---")
# # # #     st.markdown("### 📋 Upcoming Events")
# # # #     try:
# # # #         events = get_upcoming_events(5)
# # # #         if events:
# # # #             for ev in events:
# # # #                 start = ev['start'].get('dateTime', ev['start'].get('date'))
# # # #                 formatted_time = format_event_time(start)
# # # #                 st.markdown(f"**{ev.get('summary','Untitled')}**")
# # # #                 st.caption(formatted_time)
# # # #                 st.markdown("---")
# # # #         else:
# # # #             st.info("No upcoming events")
# # # #     except:
# # # #         st.warning("Could not load events")

# # # #     st.markdown("---")
# # # #     st.markdown("### 💡 How to use")
# # # #     st.markdown("- **Type date** or select from dropdown\n- Click 'View Events'\n- Type meeting requests below")
    
# # # #     if st.button("🗑️ Clear chat", use_container_width=True):
# # # #         st.session_state.messages = []
# # # #         st.session_state.pending_slot = None
# # # #         st.session_state.pending_parsed_data = None
# # # #         st.session_state.current_suggestion = None
# # # #         st.session_state.selected_alternative = None
# # # #         st.session_state._pending_confirm_msg = None
# # # #         st.rerun()
# # # # # -------------------------
# # # # # Main content header
# # # # # -------------------------
# # # # st.markdown('<div class="main-header">🤖 AI Meeting Scheduler Agent</div>', unsafe_allow_html=True)
# # # # st.markdown('<div class="sub-header">Schedule meetings using natural language</div>', unsafe_allow_html=True)

# # # # # -------------------------
# # # # # Render chat messages
# # # # # -------------------------
# # # # for msg in st.session_state.messages:
# # # #     with st.chat_message(msg["role"]):
# # # #         st.markdown(msg["content"], unsafe_allow_html=True)

# # # # # -------------------------
# # # # # Chat input -> parse -> suggest
# # # # # -------------------------
# # # # user_input = st.chat_input("Type your meeting request here... (e.g., 'Schedule meeting tomorrow at 3pm')")

# # # # if user_input:
# # # #     st.session_state.messages.append({"role":"user","content":user_input})
# # # #     with st.chat_message("user"):
# # # #         st.markdown(user_input)

# # # #     with st.chat_message("assistant"):
# # # #         with st.spinner("🔍 Analyzing your request..."):
# # # #             parsed = parse_meeting_request(user_input)
# # # #             if not parsed:
# # # #                 err = "❌ Couldn't understand. Try: 'Schedule meeting tomorrow at 3pm for 30 minutes'"
# # # #                 st.markdown(err)
# # # #                 st.session_state.messages.append({"role":"assistant","content":err})
# # # #             else:
# # # #                 suggestion = suggest_best_slot(parsed)
# # # #                 st.session_state.pending_parsed_data = parsed
# # # #                 st.session_state.current_suggestion = suggestion

# # # #                 if not suggestion.get("success"):
# # # #                     err = f"❌ {suggestion.get('message','Unable to find slots')}"
# # # #                     st.markdown(err)
# # # #                     st.session_state.messages.append({"role":"assistant","content":err})
# # # #                 else:
# # # #                     if suggestion.get("conflict"):
# # # #                         conflict = suggestion["conflict"]
# # # #                         response = f"""⚠️ **Event Conflict Detected!**

# # # # 🚫 **Existing Event at Requested Time:**
# # # # - **Event Name:** {conflict.get('summary','Untitled')}
# # # # - **Time:** {conflict['start'].strftime('%a, %b %d at %I:%M %p')} - {conflict['end'].strftime('%I:%M %p')}

# # # # ✅ **Available Alternative Slots:**
# # # # - **Title:** {parsed.get('title')}
# # # # - **Duration:** {parsed.get('duration_minutes')} minutes

# # # # 👇 Click on any available time slot below.
# # # # """
# # # #                         st.markdown(response)
# # # #                         st.session_state.messages.append({"role":"assistant","content":response})
# # # #                         st.session_state.pending_slot = None
# # # #                         st.session_state.selected_alternative = None
# # # #                     else:
# # # #                         slot = suggestion["slot"]
# # # #                         st.session_state.pending_slot = slot
# # # #                         formatted = format_slot_for_display(slot)
# # # #                         response = f"""✅ **Found slot**

# # # # 📅 **{parsed.get('title')}**
# # # # - **When:** {formatted['full_display']}
# # # # - **Duration:** {parsed.get('duration_minutes')} minutes

# # # # Click 'Confirm & Create Event' to book.
# # # # """
# # # #                         st.markdown(response)
# # # #                         st.session_state.messages.append({"role":"assistant","content":response})

# # # # # -------------------------
# # # # # Pending confirm message
# # # # # -------------------------
# # # # if st.session_state._pending_confirm_msg:
# # # #     msg = st.session_state._pending_confirm_msg
# # # #     last = st.session_state.messages[-1]["content"] if st.session_state.messages else None
# # # #     if last != msg:
# # # #         st.session_state.messages.append({"role":"assistant","content":msg})
# # # #     st.session_state._pending_confirm_msg = None

# # # # # -------------------------
# # # # # Alternative slot buttons
# # # # # -------------------------
# # # # if st.session_state.current_suggestion and st.session_state.current_suggestion.get("alternatives"):
# # # #     suggestion = st.session_state.current_suggestion
# # # #     alts = suggestion.get("alternatives", [])
# # # #     if alts:
# # # #         st.markdown("---")
# # # #         st.markdown("### 📅 Available Time Slots")
# # # #         cols = st.columns(min(3, len(alts)))
# # # #         for idx, slot in enumerate(alts):
# # # #             formatted = format_slot_for_display(slot)
# # # #             btn_key = f"alt_{idx}_{slot['start'].isoformat()}"
# # # #             clicked = cols[idx % 3].button(f"📅 {formatted['date']}\n⏰ {formatted['time_range']}", key=btn_key, use_container_width=True)
# # # #             if clicked:
# # # #                 st.session_state.pending_slot = slot
# # # #                 st.session_state.selected_alternative = idx
# # # #                 st.session_state._pending_confirm_msg = f"✅ Selected: **{formatted['full_display']}**\n\nClick 'Confirm & Create Event' below to book this slot."
# # # #                 st.rerun()

# # # # # -------------------------
# # # # # Confirmation block
# # # # # -------------------------
# # # # if st.session_state.pending_slot:
# # # #     st.markdown("---")
# # # #     col1, col2, col3 = st.columns([1, 2, 1])
# # # #     with col2:
# # # #         confirm = st.button("✅ Confirm & Create Event", type="primary", use_container_width=True, key="confirm_create")
# # # #         cancel = st.button("❌ Cancel", use_container_width=True, key="cancel_create")

# # # #         if confirm:
# # # #             with st.spinner("📅 Creating event..."):
# # # #                 if st.session_state.event_created:
# # # #                     st.info("Event already created in this session.")
# # # #                 else:
# # # #                     try:
# # # #                         slot = st.session_state.pending_slot
# # # #                         parsed = st.session_state.pending_parsed_data
# # # #                         created = create_event(
# # # #                             summary=parsed.get("title","Meeting"),
# # # #                             start_datetime=slot["start"],
# # # #                             end_datetime=slot["end"],
# # # #                             description=parsed.get("description","Created by AI Meeting Scheduler Agent"),
# # # #                             attendees=parsed.get("attendees",[])
# # # #                         )
# # # #                         if created:
# # # #                             formatted = format_slot_for_display(slot)
# # # #                             event_link = created.get('htmlLink', '#')
# # # #                             success = f"""🎉 **Event Created Successfully!**

# # # # 📅 **{parsed.get('title','Meeting')}**
# # # # - **Time:** {formatted['full_display']}

# # # # [📱 View in Google Calendar]({event_link})
# # # # """
# # # #                             st.session_state.messages.append({"role":"assistant","content":success})
# # # #                             st.session_state.pending_slot = None
# # # #                             st.session_state.pending_parsed_data = None
# # # #                             st.session_state.current_suggestion = None
# # # #                             st.session_state.selected_alternative = None
# # # #                             st.session_state.event_created = True
# # # #                             st.success("✅ Event created successfully!")
# # # #                             st.balloons()
# # # #                             st.rerun()
# # # #                         else:
# # # #                             err = "❌ Failed to create event. Try again."
# # # #                             st.session_state.messages.append({"role":"assistant","content":err})
# # # #                             st.error(err)
# # # #                     except Exception as e:
# # # #                         err = f"❌ Error creating event: {e}"
# # # #                         st.session_state.messages.append({"role":"assistant","content":err})
# # # #                         st.error(err)

# # # #         if cancel:
# # # #             st.session_state.pending_slot = None
# # # #             st.session_state.pending_parsed_data = None
# # # #             st.session_state.current_suggestion = None
# # # #             st.session_state.selected_alternative = None
# # # #             st.session_state._pending_confirm_msg = None
# # # #             cancel_msg = "❌ Meeting request cancelled. Feel free to make a new request!"
# # # #             last = st.session_state.messages[-1]["content"] if st.session_state.messages else None
# # # #             if last != cancel_msg:
# # # #                 st.session_state.messages.append({"role":"assistant","content":cancel_msg})
# # # #             st.rerun()

# # # # # Footer
# # # # st.markdown("---")
# # # # st.markdown('<div style="text-align:center;color:#666;font-size:0.9rem;">Powered by Google Calendar API | Built with Streamlit</div>', unsafe_allow_html=True)




















# # # # #everything worki g heree
# # # # import streamlit as st
# # # # from datetime import datetime, timedelta, date
# # # # import pytz
# # # # import calendar as cal_module

# # # # from scheduler.gpt_parser import parse_meeting_request, parse_datetime_from_parsed_data
# # # # from scheduler.scheduler_logic import suggest_best_slot, format_slot_for_display
# # # # from scheduler.google_calendar import create_event, get_upcoming_events




# # # # import streamlit.components.v1 as components

# # # # # Inject mic + speech recognition JS
# # # # def stt_component():
# # # #     component_html = """
# # # #     <script>
# # # #     // Create global speech recognition object
# # # #     if (!window.sttSetupDone) {
# # # #         window.sttSetupDone = true;
        
# # # #         const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
# # # #         let recognition = null;

# # # #         if (SpeechRecognition) {
# # # #             recognition = new SpeechRecognition();
# # # #             recognition.continuous = false;
# # # #             recognition.interimResults = false;
# # # #             recognition.lang = "en-US";

# # # #             recognition.onresult = function(event) {
# # # #                 const text = event.results[0][0].transcript;
# # # #                 const inputBox = window.parent.document.querySelector('textarea[placeholder*="Type your meeting request"]');
# # # #                 if (inputBox) {
# # # #                     inputBox.value = text;  // Put text inside input box
# # # #                     inputBox.dispatchEvent(new Event("input", {bubbles:true}));
# # # #                 }
# # # #             };

# # # #             recognition.onerror = function(event) {
# # # #                 console.log("STT Error:", event.error);
# # # #             };
# # # #         }

# # # #             // Add mic button next to Streamlit chat input
# # # #         function addMicButton() {
# # # #             // NEW Streamlit chat input container selector
# # # #             const inputRow = window.parent.document.querySelector('div[data-testid="stChatInput"]');

# # # #             if (!inputRow) return;

# # # #             // Prevent duplicate buttons
# # # #             if (document.getElementById("mic-btn")) return;

# # # #             // Create mic button
# # # #             const btn = document.createElement("button");
# # # #             btn.id = "mic-btn";
# # # #             btn.innerHTML = "🎤";
# # # #             btn.style.marginLeft = "6px";
# # # #             btn.style.padding = "4px 10px";
# # # #             btn.style.fontSize = "18px";
# # # #             btn.style.borderRadius = "6px";
# # # #             btn.style.cursor = "pointer";
# # # #             btn.style.border = "1px solid #ccc";
# # # #             btn.style.background = "white";

# # # #             btn.onclick = function() {
# # # #                 if (recognition) recognition.start();
# # # #             };

# # # #             // Append mic button AFTER the text area
# # # #             inputRow.appendChild(btn);
# # # #         }


# # # #         setInterval(addMicButton, 800);
# # # #     }
# # # #     </script>
# # # #     """
# # # #     components.html(component_html, height=0, width=0)





# # # # # -------------------------
# # # # # Page + session init
# # # # # -------------------------
# # # # st.set_page_config(page_title="AI Meeting Scheduler", page_icon="📅", layout="wide")

# # # # LOCAL_TZ = pytz.timezone("Asia/Kolkata")

# # # # # Initialize ALL session state at the very beginning
# # # # today = date.today()
# # # # if "current_month" not in st.session_state:
# # # #     st.session_state.current_month = today.month
# # # # if "current_year" not in st.session_state:
# # # #     st.session_state.current_year = today.year
# # # # if "messages" not in st.session_state:
# # # #     st.session_state.messages = []
# # # # if "pending_slot" not in st.session_state:
# # # #     st.session_state.pending_slot = None
# # # # if "pending_parsed_data" not in st.session_state:
# # # #     st.session_state.pending_parsed_data = None
# # # # if "current_suggestion" not in st.session_state:
# # # #     st.session_state.current_suggestion = None
# # # # if "selected_alternative" not in st.session_state:
# # # #     st.session_state.selected_alternative = None
# # # # if "event_created" not in st.session_state:
# # # #     st.session_state.event_created = False
# # # # if "_pending_confirm_msg" not in st.session_state:
# # # #     st.session_state._pending_confirm_msg = None

# # # # # -------------------------
# # # # # CALLBACK FUNCTIONS for month navigation
# # # # # -------------------------
# # # # def go_prev_month():
# # # #     if st.session_state.current_month == 1:
# # # #         st.session_state.current_month = 12
# # # #         st.session_state.current_year -= 1
# # # #     else:
# # # #         st.session_state.current_month -= 1

# # # # def go_next_month():
# # # #     if st.session_state.current_month == 12:
# # # #         st.session_state.current_month = 1
# # # #         st.session_state.current_year += 1
# # # #     else:
# # # #         st.session_state.current_month += 1

# # # # # -------------------------
# # # # # Helper function: Format datetime properly
# # # # # -------------------------
# # # # def format_event_time(event_time_str):
# # # #     """Convert ISO datetime string to readable format"""
# # # #     try:
# # # #         if 'T' in event_time_str:
# # # #             dt = datetime.fromisoformat(event_time_str.replace('Z', '+00:00'))
# # # #             dt_local = dt.astimezone(LOCAL_TZ)
# # # #             return dt_local.strftime('%a, %b %d at %I:%M %p')
# # # #         else:
# # # #             dt = datetime.strptime(event_time_str, '%Y-%m-%d')
# # # #             return dt.strftime('%a, %b %d (All day)')
# # # #     except:
# # # #         return event_time_str

# # # # def get_events_for_date(target_date):
# # # #     """Get all events for a specific date"""
# # # #     try:
# # # #         from scheduler.google_calendar import get_calendar_service
# # # #         import pytz
        
# # # #         service = get_calendar_service()
        
# # # #         start_of_day = LOCAL_TZ.localize(
# # # #             datetime.combine(target_date, datetime.min.time())
# # # #         )
# # # #         end_of_day = LOCAL_TZ.localize(
# # # #             datetime.combine(target_date, datetime.max.time())
# # # #         )
        
# # # #         time_min = start_of_day.astimezone(pytz.UTC).isoformat()
# # # #         time_max = end_of_day.astimezone(pytz.UTC).isoformat()
        
# # # #         events_result = service.events().list(
# # # #             calendarId='primary',
# # # #             timeMin=time_min,
# # # #             timeMax=time_max,
# # # #             singleEvents=True,
# # # #             orderBy='startTime'
# # # #         ).execute()
        
# # # #         events = events_result.get('items', [])
        
# # # #         formatted_events = []
# # # #         for event in events:
# # # #             start = event['start'].get('dateTime', event['start'].get('date'))
# # # #             end = event['end'].get('dateTime', event['end'].get('date'))
            
# # # #             if 'T' in start:
# # # #                 start_dt = datetime.fromisoformat(start.replace('Z', '+00:00')).astimezone(LOCAL_TZ)
# # # #                 end_dt = datetime.fromisoformat(end.replace('Z', '+00:00')).astimezone(LOCAL_TZ)
# # # #                 time_str = f"{start_dt.strftime('%I:%M %p')} - {end_dt.strftime('%I:%M %p')}"
# # # #             else:
# # # #                 time_str = "All day"
            
# # # #             formatted_events.append({
# # # #                 'summary': event.get('summary', 'Untitled'),
# # # #                 'time': time_str,
# # # #                 'description': event.get('description', '')
# # # #             })
        
# # # #         return formatted_events
# # # #     except Exception as e:
# # # #         return []

# # # # # -------------------------
# # # # # UI CSS
# # # # # -------------------------
# # # # st.markdown(
# # # #     """
# # # # <style>
# # # #     .main-header { font-size: 2.2rem; font-weight: 700; color: #1f77b4; text-align: center; margin-bottom: 6px; }
# # # #     .sub-header { font-size: 1.05rem; color: #666; text-align: center; margin-bottom: 14px; }
    
# # # #     /* Calendar Grid */
# # # #     .calendar-grid { 
# # # #         display: grid; 
# # # #         grid-template-columns: repeat(7, 1fr); 
# # # #         gap: 4px; 
# # # #         margin: 8px 0; 
# # # #     }
# # # #     .calendar-day { 
# # # #         aspect-ratio: 1; 
# # # #         display: flex; 
# # # #         align-items: center; 
# # # #         justify-content: center; 
# # # #         background: #f0f2f6; 
# # # #         border-radius: 6px; 
# # # #         font-size: 0.85rem; 
# # # #         font-weight: 500;
# # # #     }
# # # #     .calendar-header { 
# # # #         font-weight: 700; 
# # # #         background: #1f77b4; 
# # # #         color: white; 
# # # #     }
# # # #     .calendar-today { 
# # # #         background: #4CAF50; 
# # # #         color: white; 
# # # #         font-weight: 700; 
# # # #     }
# # # # </style>
# # # # """,
# # # #     unsafe_allow_html=True,
# # # # )

# # # # # -------------------------
# # # # # Sidebar (calendar + upcoming)
# # # # # -------------------------
# # # # with st.sidebar:
# # # #     st.markdown("### 📅 Meeting Scheduler")
# # # #     st.markdown("---")

# # # #     # Month navigation with CALLBACKS
# # # #     col1, col2, col3 = st.columns([1, 2, 1])
    
# # # #     col1.button("◀", key="prev_month", on_click=go_prev_month, use_container_width=True)
# # # #     col2.markdown(f"<div style='text-align:center; padding-top:8px;'><strong>{cal_module.month_name[st.session_state.current_month]} {st.session_state.current_year}</strong></div>", unsafe_allow_html=True)
# # # #     col3.button("▶", key="next_month", on_click=go_next_month, use_container_width=True)

# # # #     # Calendar display
# # # #     cal = cal_module.monthcalendar(st.session_state.current_year, st.session_state.current_month)
# # # #     calendar_html = '<div class="calendar-grid">'
    
# # # #     for day in ['Mo','Tu','We','Th','Fr','Sa','Su']:
# # # #         calendar_html += f'<div class="calendar-day calendar-header">{day}</div>'
    
# # # #     for week in cal:
# # # #         for d in week:
# # # #             if d == 0:
# # # #                 calendar_html += '<div class="calendar-day"></div>'
# # # #             else:
# # # #                 is_today = (d == today.day and 
# # # #                            st.session_state.current_month == today.month and 
# # # #                            st.session_state.current_year == today.year)
# # # #                 css = "calendar-today" if is_today else ""
# # # #                 calendar_html += f'<div class="calendar-day {css}">{d}</div>'
    
# # # #     calendar_html += '</div>'
# # # #     st.markdown(calendar_html, unsafe_allow_html=True)
    
# # # #     # Date selector
# # # #     st.markdown("---")
# # # #     st.markdown("**📅 View Events for Date:**")
    
# # # #     date_input = st.text_input(
# # # #         "Type date (DD/MM/YYYY)",
# # # #         placeholder="28/11/2025",
# # # #         key="manual_date_input",
# # # #         help="Enter date in DD/MM/YYYY format"
# # # #     )
    
# # # #     if st.button("📅 View Events", use_container_width=True, key="view_events_btn"):
# # # #         selected_date = None
        
# # # #         if date_input.strip():
# # # #             try:
# # # #                 parts = date_input.strip().split('/')
# # # #                 if len(parts) == 3:
# # # #                     day, month, year = int(parts[0]), int(parts[1]), int(parts[2])
# # # #                     selected_date = date(year, month, day)
# # # #             except:
# # # #                 st.error("❌ Invalid format! Use DD/MM/YYYY (e.g., 28/11/2025)")
        
# # # #         if selected_date:
# # # #             events = get_events_for_date(selected_date)
            
# # # #             st.markdown(f"**📆 {selected_date.strftime('%A, %B %d, %Y')}**")
# # # #             st.markdown("---")
            
# # # #             if events:
# # # #                 for event in events:
# # # #                     st.markdown(f"### 🕐 {event['time']}")
# # # #                     st.markdown(f"**{event['summary']}**")
# # # #                     if event.get('description'):
# # # #                         st.caption(event['description'])
# # # #                     st.markdown("---")
# # # #             else:
# # # #                 st.info(f"✨ No events on {selected_date.strftime('%B %d')}")
# # # #         else:
# # # #             st.warning("⚠️ Please enter a date in DD/MM/YYYY format")

# # # #     st.markdown("---")
# # # #     st.markdown("### 📋 Upcoming Events")
# # # #     try:
# # # #         events = get_upcoming_events(5)
# # # #         if events:
# # # #             for ev in events:
# # # #                 start = ev['start'].get('dateTime', ev['start'].get('date'))
# # # #                 formatted_time = format_event_time(start)
# # # #                 st.markdown(f"**{ev.get('summary','Untitled')}**")
# # # #                 st.caption(formatted_time)
# # # #                 st.markdown("---")
# # # #         else:
# # # #             st.info("No upcoming events")
# # # #     except:
# # # #         st.warning("Could not load events")

# # # #     st.markdown("---")
# # # #     st.markdown("### 💡 How to use")
# # # #     st.markdown("- **Type date** in DD/MM/YYYY format\n- Click 'View Events'\n- Type meeting requests below")
    
# # # #     if st.button("🗑️ Clear chat", use_container_width=True):
# # # #         st.session_state.messages = []
# # # #         st.session_state.pending_slot = None
# # # #         st.session_state.pending_parsed_data = None
# # # #         st.session_state.current_suggestion = None
# # # #         st.session_state.selected_alternative = None
# # # #         st.session_state._pending_confirm_msg = None
# # # #         st.rerun()

# # # # # -------------------------
# # # # # Main content header
# # # # # -------------------------
# # # # st.markdown('<div class="main-header">🤖 AI Meeting Scheduler Agent</div>', unsafe_allow_html=True)
# # # # st.markdown('<div class="sub-header">Schedule meetings using natural language</div>', unsafe_allow_html=True)

# # # # # -------------------------
# # # # # Render chat messages
# # # # # -------------------------
# # # # for msg in st.session_state.messages:
# # # #     with st.chat_message(msg["role"]):
# # # #         st.markdown(msg["content"], unsafe_allow_html=True)

# # # # # -------------------------
# # # # # Chat input -> parse -> suggest
# # # # # -------------------------


# # # # # Inject STT microphone functionality
# # # # stt_component()

# # # # user_input = st.chat_input("Type your meeting request here... (e.g., 'Schedule meeting tomorrow at 3pm')")

# # # # if user_input:
# # # #     st.session_state.messages.append({"role":"user","content":user_input})
# # # #     with st.chat_message("user"):
# # # #         st.markdown(user_input)

# # # #     with st.chat_message("assistant"):
# # # #         with st.spinner("🔍 Analyzing your request..."):
# # # #             parsed = parse_meeting_request(user_input)
# # # #             if not parsed:
# # # #                 err = "❌ Couldn't understand. Try: 'Schedule meeting tomorrow at 3pm for 30 minutes'"
# # # #                 st.markdown(err)
# # # #                 st.session_state.messages.append({"role":"assistant","content":err})
# # # #             else:
# # # #                 suggestion = suggest_best_slot(parsed)
# # # #                 st.session_state.pending_parsed_data = parsed
# # # #                 st.session_state.current_suggestion = suggestion

# # # #                 if not suggestion.get("success"):
# # # #                     err = f"❌ {suggestion.get('message','Unable to find slots')}"
# # # #                     st.markdown(err)
# # # #                     st.session_state.messages.append({"role":"assistant","content":err})
# # # #                 else:
# # # #                     if suggestion.get("conflict"):
# # # #                         conflict = suggestion["conflict"]
# # # #                         response = f"""⚠️ **Event Conflict Detected!**

# # # # 🚫 **Existing Event at Requested Time:**
# # # # - **Event Name:** {conflict.get('summary','Untitled')}
# # # # - **Time:** {conflict['start'].strftime('%a, %b %d at %I:%M %p')} - {conflict['end'].strftime('%I:%M %p')}

# # # # ✅ **Available Alternative Slots:**
# # # # - **Title:** {parsed.get('title')}
# # # # - **Duration:** {parsed.get('duration_minutes')} minutes

# # # # 👇 Click on any available time slot below.
# # # # """
# # # #                         st.markdown(response)
# # # #                         st.session_state.messages.append({"role":"assistant","content":response})
# # # #                         st.session_state.pending_slot = None
# # # #                         st.session_state.selected_alternative = None
# # # #                     else:
# # # #                         slot = suggestion["slot"]
# # # #                         st.session_state.pending_slot = slot
# # # #                         formatted = format_slot_for_display(slot)
# # # #                         response = f"""✅ **Found slot**

# # # # 📅 **{parsed.get('title')}**
# # # # - **When:** {formatted['full_display']}
# # # # - **Duration:** {parsed.get('duration_minutes')} minutes

# # # # Click 'Confirm & Create Event' to book.
# # # # """
# # # #                         st.markdown(response)
# # # #                         st.session_state.messages.append({"role":"assistant","content":response})

# # # # # -------------------------
# # # # # Pending confirm message
# # # # # -------------------------
# # # # if st.session_state._pending_confirm_msg:
# # # #     msg = st.session_state._pending_confirm_msg
# # # #     last = st.session_state.messages[-1]["content"] if st.session_state.messages else None
# # # #     if last != msg:
# # # #         st.session_state.messages.append({"role":"assistant","content":msg})
# # # #     st.session_state._pending_confirm_msg = None

# # # # # -------------------------
# # # # # Alternative slot buttons
# # # # # -------------------------
# # # # if st.session_state.current_suggestion and st.session_state.current_suggestion.get("alternatives"):
# # # #     suggestion = st.session_state.current_suggestion
# # # #     alts = suggestion.get("alternatives", [])
# # # #     if alts:
# # # #         st.markdown("---")
# # # #         st.markdown("### 📅 Available Time Slots")
# # # #         cols = st.columns(min(3, len(alts)))
# # # #         for idx, slot in enumerate(alts):
# # # #             formatted = format_slot_for_display(slot)
# # # #             btn_key = f"alt_{idx}_{slot['start'].isoformat()}"
# # # #             clicked = cols[idx % 3].button(f"📅 {formatted['date']}\n⏰ {formatted['time_range']}", key=btn_key, use_container_width=True)
# # # #             if clicked:
# # # #                 st.session_state.pending_slot = slot
# # # #                 st.session_state.selected_alternative = idx
# # # #                 st.session_state._pending_confirm_msg = f"✅ Selected: **{formatted['full_display']}**\n\nClick 'Confirm & Create Event' below to book this slot."
# # # #                 st.rerun()

# # # # # -------------------------
# # # # # Confirmation block
# # # # # -------------------------
# # # # if st.session_state.pending_slot:
# # # #     st.markdown("---")
# # # #     col1, col2, col3 = st.columns([1, 2, 1])
# # # #     with col2:
# # # #         confirm = st.button("✅ Confirm & Create Event", type="primary", use_container_width=True, key="confirm_create")
# # # #         cancel = st.button("❌ Cancel", use_container_width=True, key="cancel_create")

# # # #         if confirm:
# # # #             with st.spinner("📅 Creating event..."):
# # # #                 if st.session_state.event_created:
# # # #                     st.info("Event already created in this session.")
# # # #                 else:
# # # #                     try:
# # # #                         slot = st.session_state.pending_slot
# # # #                         parsed = st.session_state.pending_parsed_data
# # # #                         created = create_event(
# # # #                             summary=parsed.get("title","Meeting"),
# # # #                             start_datetime=slot["start"],
# # # #                             end_datetime=slot["end"],
# # # #                             description=parsed.get("description","Created by AI Meeting Scheduler Agent"),
# # # #                             attendees=parsed.get("attendees",[])
# # # #                         )
# # # #                         if created:
# # # #                             formatted = format_slot_for_display(slot)
# # # #                             event_link = created.get('htmlLink', '#')
# # # #                             success = f"""🎉 **Event Created Successfully!**

# # # # 📅 **{parsed.get('title','Meeting')}**
# # # # - **Time:** {formatted['full_display']}

# # # # [📱 View in Google Calendar]({event_link})
# # # # """
# # # #                             st.session_state.messages.append({"role":"assistant","content":success})
# # # #                             st.session_state.pending_slot = None
# # # #                             st.session_state.pending_parsed_data = None
# # # #                             st.session_state.current_suggestion = None
# # # #                             st.session_state.selected_alternative = None
# # # #                             st.session_state.event_created = True
# # # #                             st.success("✅ Event created successfully!")
# # # #                             st.balloons()
# # # #                             st.rerun()
# # # #                         else:
# # # #                             err = "❌ Failed to create event. Try again."
# # # #                             st.session_state.messages.append({"role":"assistant","content":err})
# # # #                             st.error(err)
# # # #                     except Exception as e:
# # # #                         err = f"❌ Error creating event: {e}"
# # # #                         st.session_state.messages.append({"role":"assistant","content":err})
# # # #                         st.error(err)

# # # #         if cancel:
# # # #             st.session_state.pending_slot = None
# # # #             st.session_state.pending_parsed_data = None
# # # #             st.session_state.current_suggestion = None
# # # #             st.session_state.selected_alternative = None
# # # #             st.session_state._pending_confirm_msg = None
# # # #             cancel_msg = "❌ Meeting request cancelled. Feel free to make a new request!"
# # # #             last = st.session_state.messages[-1]["content"] if st.session_state.messages else None
# # # #             if last != cancel_msg:
# # # #                 st.session_state.messages.append({"role":"assistant","content":cancel_msg})
# # # #             st.rerun()

# # # # # Footer
# # # # st.markdown("---")
# # # # st.markdown('<div style="text-align:center;color:#666;font-size:0.9rem;">Powered by Google Calendar API | Built with Streamlit</div>', unsafe_allow_html=True)















# # # #everything worki g heree..changing ui a bit
# # # import streamlit as st
# # # from datetime import datetime, timedelta, date
# # # import pytz
# # # import calendar as cal_module

# # # from scheduler.gpt_parser import parse_meeting_request, parse_datetime_from_parsed_data
# # # from scheduler.scheduler_logic import suggest_best_slot, format_slot_for_display
# # # from scheduler.google_calendar import create_event, get_upcoming_events




# # # import streamlit.components.v1 as components

# # # # Inject mic + speech recognition JS
# # # def stt_component():
# # #     component_html = """
# # #     <script>
# # #     // Create global speech recognition object
# # #     if (!window.sttSetupDone) {
# # #         window.sttSetupDone = true;
        
# # #         const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
# # #         let recognition = null;

# # #         if (SpeechRecognition) {
# # #             recognition = new SpeechRecognition();
# # #             recognition.continuous = false;
# # #             recognition.interimResults = false;
# # #             recognition.lang = "en-US";

# # # recognition.onresult = function(event) {
# # #                 const text = event.results[0][0].transcript;
                
# # #                 // DEBUG: Log what was transcribed
# # #                 console.log("🎤 Transcribed text:", text);
# # #                 console.log("🎤 Text length:", text.length);
# # #                 console.log("🎤 Text characters:", Array.from(text).map(c => c.charCodeAt(0)));
                
# # #                 const inputBox = window.parent.document.querySelector('textarea[data-testid="stChatInputTextArea"]');

# # #                 if (inputBox) {
# # #                     // Set the value using React's internal setter
# # #                     const nativeInputValueSetter = Object.getOwnPropertyDescriptor(
# # #                         window.HTMLTextAreaElement.prototype, 
# # #                         "value"
# # #                     ).set;
# # #                     nativeInputValueSetter.call(inputBox, text);
                    
# # #                     // Trigger multiple events to ensure Streamlit recognizes the change
# # #                     inputBox.dispatchEvent(new Event("input", {bubbles: true}));
# # #                     inputBox.dispatchEvent(new Event("change", {bubbles: true}));
                    
# # #                     // Focus the input so user can press Enter to send
# # #                     inputBox.focus();
# # #                 }
# # #             };

# # #             recognition.onerror = function(event) {
# # #                 console.log("STT Error:", event.error);
# # #             };
# # #         }

# # #             // Add mic button next to Streamlit chat input
# # #         function addMicButton() {
# # #             // NEW Streamlit chat input container selector
# # #             const inputRow = window.parent.document.querySelector('div[data-testid="stChatInput"]');

# # #             if (!inputRow) return;

# # #             // Prevent duplicate buttons
# # #             const alreadyExists = window.parent.document.querySelector("#mic-btn");
# # # if (alreadyExists) return;


# # #             // Create mic button
# # #             const btn = document.createElement("button");
# # #             btn.id = "mic-btn";
# # #             btn.innerHTML = "🎤";
# # #             btn.style.marginLeft = "6px";
# # #             btn.style.padding = "4px 10px";
# # #             btn.style.fontSize = "18px";
# # #             btn.style.borderRadius = "6px";
# # #             btn.style.cursor = "pointer";
# # #             btn.style.border = "1px solid #ccc";
# # #             btn.style.background = "white";

# # #             let listening = false;

# # # btn.onclick = function () {
# # #     if (!recognition) return;

# # #     if (!listening) {
# # #         recognition.start();
# # #         listening = true;
# # #         btn.innerHTML = "🛑";
# # #         btn.style.background = "#ffcccc";
# # #     } else {
# # #         recognition.stop();
# # #         listening = false;
# # #         btn.innerHTML = "🎤";
# # #         btn.style.background = "white";
# # #     }
# # # };


# # #             // Append mic button AFTER the text area
# # #             inputRow.appendChild(btn);
# # #         }


# # #         setInterval(addMicButton, 800);
# # #     }
# # #     </script>
# # #     """
# # #     components.html(component_html, height=0, width=0)





# # # # -------------------------
# # # # Page + session init
# # # # -------------------------
# # # st.set_page_config(page_title="AI Meeting Scheduler", page_icon="📅", layout="wide")

# # # LOCAL_TZ = pytz.timezone("Asia/Kolkata")

# # # # Initialize ALL session state at the very beginning
# # # today = date.today()
# # # if "current_month" not in st.session_state:
# # #     st.session_state.current_month = today.month
# # # if "current_year" not in st.session_state:
# # #     st.session_state.current_year = today.year
# # # if "messages" not in st.session_state:
# # #     st.session_state.messages = []
# # # if "pending_slot" not in st.session_state:
# # #     st.session_state.pending_slot = None
# # # if "pending_parsed_data" not in st.session_state:
# # #     st.session_state.pending_parsed_data = None
# # # if "current_suggestion" not in st.session_state:
# # #     st.session_state.current_suggestion = None
# # # if "selected_alternative" not in st.session_state:
# # #     st.session_state.selected_alternative = None
# # # if "event_created" not in st.session_state:
# # #     st.session_state.event_created = False
# # # if "_pending_confirm_msg" not in st.session_state:
# # #     st.session_state._pending_confirm_msg = None

# # # # -------------------------
# # # # CALLBACK FUNCTIONS for month navigation
# # # # -------------------------
# # # def go_prev_month():
# # #     if st.session_state.current_month == 1:
# # #         st.session_state.current_month = 12
# # #         st.session_state.current_year -= 1
# # #     else:
# # #         st.session_state.current_month -= 1

# # # def go_next_month():
# # #     if st.session_state.current_month == 12:
# # #         st.session_state.current_month = 1
# # #         st.session_state.current_year += 1
# # #     else:
# # #         st.session_state.current_month += 1

# # # # -------------------------
# # # # Helper function: Format datetime properly
# # # # -------------------------
# # # def format_event_time(event_time_str):
# # #     """Convert ISO datetime string to readable format"""
# # #     try:
# # #         if 'T' in event_time_str:
# # #             dt = datetime.fromisoformat(event_time_str.replace('Z', '+00:00'))
# # #             dt_local = dt.astimezone(LOCAL_TZ)
# # #             return dt_local.strftime('%a, %b %d at %I:%M %p')
# # #         else:
# # #             dt = datetime.strptime(event_time_str, '%Y-%m-%d')
# # #             return dt.strftime('%a, %b %d (All day)')
# # #     except:
# # #         return event_time_str

# # # def get_events_for_date(target_date):
# # #     """Get all events for a specific date"""
# # #     try:
# # #         from scheduler.google_calendar import get_calendar_service
# # #         import pytz
        
# # #         service = get_calendar_service()
        
# # #         start_of_day = LOCAL_TZ.localize(
# # #             datetime.combine(target_date, datetime.min.time())
# # #         )
# # #         end_of_day = LOCAL_TZ.localize(
# # #             datetime.combine(target_date, datetime.max.time())
# # #         )
        
# # #         time_min = start_of_day.astimezone(pytz.UTC).isoformat()
# # #         time_max = end_of_day.astimezone(pytz.UTC).isoformat()
        
# # #         events_result = service.events().list(
# # #             calendarId='primary',
# # #             timeMin=time_min,
# # #             timeMax=time_max,
# # #             singleEvents=True,
# # #             orderBy='startTime'
# # #         ).execute()
        
# # #         events = events_result.get('items', [])
        
# # #         formatted_events = []
# # #         for event in events:
# # #             start = event['start'].get('dateTime', event['start'].get('date'))
# # #             end = event['end'].get('dateTime', event['end'].get('date'))
            
# # #             if 'T' in start:
# # #                 start_dt = datetime.fromisoformat(start.replace('Z', '+00:00')).astimezone(LOCAL_TZ)
# # #                 end_dt = datetime.fromisoformat(end.replace('Z', '+00:00')).astimezone(LOCAL_TZ)
# # #                 time_str = f"{start_dt.strftime('%I:%M %p')} - {end_dt.strftime('%I:%M %p')}"
# # #             else:
# # #                 time_str = "All day"
            
# # #             formatted_events.append({
# # #                 'summary': event.get('summary', 'Untitled'),
# # #                 'time': time_str,
# # #                 'description': event.get('description', '')
# # #             })
        
# # #         return formatted_events
# # #     except Exception as e:
# # #         return []

# # # # -------------------------
# # # # UI CSS
# # # # -------------------------
# # # st.markdown(
# # #     """
# # # <style>






# # # /* Add these CSS rules to your st.markdown() style block */

# # # /* Make top header bar dark with visible buttons */
# # # header[data-testid="stHeader"] {
# # #     background-color: rgba(15, 12, 41, 0.95) !important;
# # #     backdrop-filter: blur(10px) !important;
# # # }

# # # /* Ensure Deploy button and menu are visible */
# # # header[data-testid="stHeader"] button,
# # # header[data-testid="stHeader"] a {
# # #     color: #e0e0e0 !important;
# # #     opacity: 1 !important;
# # # }

# # # /* Bottom container - DARK background */
# # # .stChatFloatingInputContainer {
# # #     background: rgba(15, 12, 41, 0.95) !important;
# # #     backdrop-filter: blur(15px) !important;
# # #     border-top: 1px solid rgba(255, 255, 255, 0.1) !important;
# # #     padding: 20px !important;
# # # }

# # # /* ONLY the input box itself is WHITE */
# # # .stChatInputContainer > div {
# # #     background: white !important;
# # #     border: 1px solid rgba(0, 0, 0, 0.15) !important;
# # #     border-radius: 24px !important;
# # #     box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1) !important;
# # # }

# # # /* Textarea - dark text on white background */
# # # textarea[data-testid="stChatInputTextArea"] {
# # #     background: white !important;
# # #     color: #1a1a1a !important;
# # #     border: none !important;
# # # }

# # # textarea[data-testid="stChatInputTextArea"]::placeholder {
# # #     color: rgba(0, 0, 0, 0.5) !important;
# # # }

# # # /* Send button and other controls - keep visible */
# # # .stChatInputContainer button {
# # #     color: #666 !important;
# # # }






# # #     /* Global Dark Theme - Fixed blur issue */
# # #     .stApp {
# # #         background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%) !important;
# # #         background-attachment: fixed !important;
# # #     }
    
# # #     /* Main content area - remove any conflicting backgrounds */
# # #     # .main .block-container {
# # #     #     background: transparent !important;
# # #     # }
    
# # #     /* Sidebar Glassmorphism */
# # #     section[data-testid="stSidebar"] {
# # #         background: rgba(255, 255, 255, 0.05) !important;
# # #         backdrop-filter: blur(10px) !important;
# # #         border-right: 1px solid rgba(255, 255, 255, 0.1) !important;
# # #     }
    
# # #     section[data-testid="stSidebar"] * {
# # #         color: #e0e0e0 !important;
# # #     }
    
# # #     /* Headers */
# # #     .main-header { 
# # #         font-size: 2.5rem; 
# # #         font-weight: 700; 
# # #         background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
# # #         -webkit-background-clip: text;
# # #         -webkit-text-fill-color: transparent;
# # #         text-align: center; 
# # #         margin-bottom: 8px;
# # #         text-shadow: 0 0 30px rgba(102, 126, 234, 0.3);
# # #     }
    
# # #     .sub-header { 
# # #         font-size: 1.1rem; 
# # #         color: #b0b0b0; 
# # #         text-align: center; 
# # #         margin-bottom: 20px;
# # #         font-weight: 300;
# # #     }
    
# # #     /* Calendar Grid - Glassmorphism */
# # #     .calendar-grid { 
# # #         display: grid; 
# # #         grid-template-columns: repeat(7, 1fr); 
# # #         gap: 6px; 
# # #         margin: 12px 0;
# # #         padding: 15px;
# # #         background: rgba(255, 255, 255, 0.03);
# # #         backdrop-filter: blur(10px);
# # #         border-radius: 16px;
# # #         border: 1px solid rgba(255, 255, 255, 0.1);
# # #     }
    
# # #     .calendar-day { 
# # #         aspect-ratio: 1; 
# # #         display: flex; 
# # #         align-items: center; 
# # #         justify-content: center; 
# # #         background: rgba(255, 255, 255, 0.05); 
# # #         border-radius: 10px; 
# # #         font-size: 0.9rem; 
# # #         font-weight: 500;
# # #         border: 1px solid rgba(255, 255, 255, 0.05);
# # #         transition: all 0.3s ease;
# # #     }
    
# # #     .calendar-day:hover {
# # #         background: rgba(102, 126, 234, 0.2);
# # #         transform: scale(1.05);
# # #     }
    
# # #     .calendar-header { 
# # #         font-weight: 700; 
# # #         background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
# # #         color: white;
# # #         border: none;
# # #     }
    
# # #     .calendar-today { 
# # #         background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
# # #         color: black; 
# # #         font-weight: 700;
# # #         box-shadow: 0 4px 15px rgba(245, 87, 108, 0.4);
# # #     }
    
# # #     /* Sidebar Containers - Blue for View Events */
# # #     section[data-testid="stSidebar"] > div:nth-child(1) > div:nth-child(1) > div:nth-child(5) {
# # #         background: rgba(102, 126, 234, 0.15) !important;
# # #         backdrop-filter: blur(15px) !important;
# # #         -webkit-backdrop-filter: blur(15px) !important;
# # #         border-radius: 20px !important;
# # #         padding: 25px !important;
# # #         margin: 20px 10px !important;
# # #         border: 2px solid rgba(102, 126, 234, 0.4) !important;
# # #         box-shadow: 0 8px 32px rgba(102, 126, 234, 0.25) !important;
# # #     }
    
# # #     /* Sidebar Containers - Purple for Upcoming Events */
# # #     section[data-testid="stSidebar"] > div:nth-child(1) > div:nth-child(1) > div:nth-child(7) {
# # #         background: rgba(118, 75, 162, 0.15) !important;
# # #         backdrop-filter: blur(15px) !important;
# # #         -webkit-backdrop-filter: blur(15px) !important;
# # #         border-radius: 20px !important;
# # #         padding: 25px !important;
# # #         margin: 20px 10px !important;
# # #         border: 2px solid rgba(118, 75, 162, 0.4) !important;
# # #         box-shadow: 0 8px 32px rgba(118, 75, 162, 0.25) !important;
# # #     }
    
# # #     /* Target divs with blue and purple glass classes */
# # #     .blue-glass-section {
# # #         background: rgba(102, 126, 234, 0.15) !important;
# # #         backdrop-filter: blur(15px) !important;
# # #         -webkit-backdrop-filter: blur(15px) !important;
# # #         border-radius: 20px !important;
# # #         padding: 25px !important;
# # #         margin: 20px 0 !important;
# # #         border: 2px solid rgba(102, 126, 234, 0.4) !important;
# # #         box-shadow: 0 8px 32px rgba(102, 126, 234, 0.25) !important;
# # #     }
    
# # #     .purple-glass-section {
# # #         background: rgba(118, 75, 162, 0.15) !important;
# # #         backdrop-filter: blur(15px) !important;
# # #         -webkit-backdrop-filter: blur(15px) !important;
# # #         border-radius: 20px !important;
# # #         padding: 25px !important;
# # #         margin: 20px 0 !important;
# # #         border: 2px solid rgba(118, 75, 162, 0.4) !important;
# # #         box-shadow: 0 8px 32px rgba(118, 75, 162, 0.25) !important;
# # #     }
    
# # #     /* Event Cards */
# # #     .event-card {
# # #         background: rgba(255, 255, 255, 0.05);
# # #         backdrop-filter: blur(5px);
# # #         border-radius: 12px;
# # #         padding: 15px;
# # #         margin: 10px 0;
# # #         border-left: 4px solid #667eea;
# # #         transition: all 0.3s ease;
# # #     }
    
# # #     .event-card:hover {
# # #         background: rgba(255, 255, 255, 0.08);
# # #         transform: translateX(5px);
# # #         box-shadow: 0 4px 20px rgba(102, 126, 234, 0.3);
# # #     }
    
# # #     /* Buttons - Glassmorphism */
# # #     .stButton > button {
# # #         background: rgba(255, 255, 255, 0.1) !important;
# # #         backdrop-filter: blur(10px) !important;
# # #         border: 1px solid rgba(255, 255, 255, 0.2) !important;
# # #         border-radius: 12px !important;
# # #         color: #e0e0e0 !important;
# # #         font-weight: 500 !important;
# # #         transition: all 0.3s ease !important;
# # #     }
    
# # #     .stButton > button:hover {
# # #         background: rgba(102, 126, 234, 0.3) !important;
# # #         border-color: rgba(102, 126, 234, 0.5) !important;
# # #         transform: translateY(-2px);
# # #         box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4) !important;
# # #     }
    
# # #     /* Primary Button */
# # #     .stButton > button[kind="primary"] {
# # #         background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
# # #         border: none !important;
# # #         color: white !important;
# # #         font-weight: 600 !important;
# # #     }
    
# # #     .stButton > button[kind="primary"]:hover {
# # #         background: linear-gradient(135deg, #764ba2 0%, #667eea 100%) !important;
# # #         box-shadow: 0 6px 25px rgba(102, 126, 234, 0.6) !important;
# # #     }
    
# # #     /* Input Fields */
# # #     .stTextInput > div > div > input {
# # #         background: rgba(255, 255, 255, 0.1) !important;
# # #         backdrop-filter: blur(10px) !important;
# # #         border: 1px solid rgba(255, 255, 255, 0.2) !important;
# # #         border-radius: 12px !important;
# # #         color: black !important;
# # #         font-weight: 500 !important;
# # #     }
    
# # #     .stTextInput > div > div > input::placeholder {
# # #         color: rgba(255, 255, 255, 0.5) !important;
# # #     }
    
# # #     /* Chat Messages */
# # #     .stChatMessage {
# # #         background: rgba(255, 255, 255, 0.05) !important;
# # #         backdrop-filter: blur(10px) !important;
# # #         border: 1px solid rgba(255, 255, 255, 0.1) !important;
# # #         border-radius: 16px !important;
# # #     }
    
# # #     /* Markdown in dark mode */
# # #     .stMarkdown {
# # #         color: #e0e0e0 !important;
# # #     }
    
# # #     /* Dividers */
# # #     hr {
# # #         border-color: rgba(255, 255, 255, 0.1) !important;
# # #         margin: 20px 0 !important;
# # #     }
    
# # #     /* Section Headers */
# # #     h3 {
# # #         color: #b0b0b0 !important;
# # #         font-weight: 600 !important;
# # #         margin-top: 15px !important;
# # #     }
    
# # #     /* Info/Warning boxes */
# # #     .stInfo, .stWarning, .stSuccess {
# # #         background: rgba(255, 255, 255, 0.05) !important;
# # #         backdrop-filter: blur(10px) !important;
# # #         border-radius: 12px !important;
# # #         border-left: 4px solid #667eea !important;
# # #     }









# # # /* ---------- FIX: extend main gradient + remove bottom glass strip ---------- */

# # # /* Make the main app gradient extend to entire page and container */
# # # .stApp,
# # # .main .block-container {
# # #   background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%) !important;
# # #   background-attachment: fixed !important;
# # # }

# # # /* Extend same background to the full body (including chat input area) */
# # # section.main > div.block-container {
# # #     background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%) !important;
# # #     background-attachment: fixed !important;
# # # }


# # # /* Remove the dark/glass overlay behind the floating chat input */
# # # .stChatFloatingInputContainer,
# # # .stChatWrapper,
# # # .stChatFooter {
# # #   background: transparent !important;
# # #   backdrop-filter: none !important;
# # #   -webkit-backdrop-filter: none !important;
# # #   border-top: none !important;
# # #   box-shadow: none !important;
# # # }

# # # /* Ensure the chat input box itself stays white and usable */
# # # .stChatInputContainer > div,
# # # textarea[data-testid="stChatInputTextArea"] {
# # #   background: white !important;
# # #   color: #111 !important;
# # #   border: 1px solid rgba(0,0,0,0.12) !important;
# # #   border-radius: 20px !important;
# # #   box-shadow: 0 2px 8px rgba(0,0,0,0.08) !important;
# # # }

# # # /* If Streamlit uses slightly different naming on your version, add these too */
# # # .stChatInput,
# # # .stChatInputContainer {
# # #   background: transparent !important;
# # # }

# # # /* Small safety: make sure no earlier rule forces opacity on the emoji/inline icons */
# # # .stMarkdown img, .stMarkdown svg, .main-header img {
# # #   background: transparent !important;
# # #   filter: none !important;
# # # }


# # # .stChatFloatingInputContainer {
# # #     background: transparent !important;
# # #     backdrop-filter: none !important;
# # #     border-top: none !important;
# # #     padding: 20px !important;
# # # }




    
# # # </style>
# # # """,
# # #     unsafe_allow_html=True,
# # # )

# # # # -------------------------
# # # # Sidebar (calendar + upcoming)
# # # # -------------------------
# # # with st.sidebar:
# # #     st.markdown("### 📅 Meeting Scheduler")
# # #     st.markdown("---")

# # #     # Month navigation with CALLBACKS
# # #     col1, col2, col3 = st.columns([1, 2, 1])
    
# # #     col1.button("◀", key="prev_month", on_click=go_prev_month, use_container_width=True)
# # #     col2.markdown(f"<div style='text-align:center; padding-top:8px;'><strong>{cal_module.month_name[st.session_state.current_month]} {st.session_state.current_year}</strong></div>", unsafe_allow_html=True)
# # #     col3.button("▶", key="next_month", on_click=go_next_month, use_container_width=True)

# # #     # Calendar display
# # #     cal = cal_module.monthcalendar(st.session_state.current_year, st.session_state.current_month)
# # #     calendar_html = '<div class="calendar-grid">'
    
# # #     for day in ['Mo','Tu','We','Th','Fr','Sa','Su']:
# # #         calendar_html += f'<div class="calendar-day calendar-header">{day}</div>'
    
# # #     for week in cal:
# # #         for d in week:
# # #             if d == 0:
# # #                 calendar_html += '<div class="calendar-day"></div>'
# # #             else:
# # #                 is_today = (d == today.day and 
# # #                            st.session_state.current_month == today.month and 
# # #                            st.session_state.current_year == today.year)
# # #                 css = "calendar-today" if is_today else ""
# # #                 calendar_html += f'<div class="calendar-day {css}">{d}</div>'
    
# # #     calendar_html += '</div>'
# # #     st.markdown(calendar_html, unsafe_allow_html=True)
    
# # #     # Date selector
# # #     st.markdown("---")
# # #     st.markdown("**📅 View Events for Date:**")
    
# # #     date_input = st.text_input(
# # #         "Type date (DD/MM/YYYY)",
# # #         placeholder="28/11/2025",
# # #         key="manual_date_input",
# # #         help="Enter date in DD/MM/YYYY format"
# # #     )
    
# # #     if st.button("📅 View Events", use_container_width=True, key="view_events_btn"):
# # #         selected_date = None
        
# # #         if date_input.strip():
# # #             try:
# # #                 parts = date_input.strip().split('/')
# # #                 if len(parts) == 3:
# # #                     day, month, year = int(parts[0]), int(parts[1]), int(parts[2])
# # #                     selected_date = date(year, month, day)
# # #             except:
# # #                 st.error("❌ Invalid format! Use DD/MM/YYYY (e.g., 28/11/2025)")
        
# # #         if selected_date:
# # #             events = get_events_for_date(selected_date)
            
# # #             st.markdown(f"**📆 {selected_date.strftime('%A, %B %d, %Y')}**")
# # #             st.markdown("---")
            
# # #             if events:
# # #                 for event in events:
# # #                     st.markdown(f"### 🕐 {event['time']}")
# # #                     st.markdown(f"**{event['summary']}**")
# # #                     if event.get('description'):
# # #                         st.caption(event['description'])
# # #                     st.markdown("---")
# # #             else:
# # #                 st.info(f"✨ No events on {selected_date.strftime('%B %d')}")
# # #         else:
# # #             st.warning("⚠️ Please enter a date in DD/MM/YYYY format")

# # #     st.markdown("---")
# # #     st.markdown("### 📋 Upcoming Events")
# # #     try:
# # #         events = get_upcoming_events(5)
# # #         if events:
# # #             for ev in events:
# # #                 start = ev['start'].get('dateTime', ev['start'].get('date'))
# # #                 formatted_time = format_event_time(start)
# # #                 st.markdown(f"**{ev.get('summary','Untitled')}**")
# # #                 st.caption(formatted_time)
# # #                 st.markdown("---")
# # #         else:
# # #             st.info("No upcoming events")
# # #     except:
# # #         st.warning("Could not load events")

# # #     st.markdown("---")
# # #     st.markdown("### 💡 How to use")
# # #     st.markdown("- **Type date** in DD/MM/YYYY format\n- Click 'View Events'\n- Type meeting requests below")
    
# # #     if st.button("🗑️ Clear chat", use_container_width=True):
# # #         st.session_state.messages = []
# # #         st.session_state.pending_slot = None
# # #         st.session_state.pending_parsed_data = None
# # #         st.session_state.current_suggestion = None
# # #         st.session_state.selected_alternative = None
# # #         st.session_state._pending_confirm_msg = None
# # #         st.rerun()

# # # # -------------------------
# # # # Main content header
# # # # -------------------------
# # # st.markdown('<div class="main-header"> AI Meeting Scheduler Agent</div>', unsafe_allow_html=True)
# # # st.markdown('<div class="sub-header">Schedule meetings using natural language</div>', unsafe_allow_html=True)

# # # # -------------------------
# # # # Render chat messages
# # # # -------------------------
# # # for msg in st.session_state.messages:
# # #     with st.chat_message(msg["role"]):
# # #         st.markdown(msg["content"], unsafe_allow_html=True)

# # # # -------------------------
# # # # Chat input -> parse -> suggest
# # # # -------------------------


# # # # Inject STT microphone functionality
# # # stt_component()

# # # user_input = st.chat_input("Type your meeting request here... (e.g., 'Schedule meeting tomorrow at 3pm')")

# # # if user_input:
# # #     st.session_state.messages.append({"role":"user","content":user_input})
# # #     with st.chat_message("user"):
# # #         st.markdown(user_input)

# # #     with st.chat_message("assistant"):
# # #         with st.spinner("🔍 Analyzing your request..."):
# # #             parsed = parse_meeting_request(user_input)
# # #             if not parsed:
# # #                 err = "❌ Couldn't understand. Try: 'Schedule meeting tomorrow at 3pm for 30 minutes'"
# # #                 st.markdown(err)
# # #                 st.session_state.messages.append({"role":"assistant","content":err})
# # #             else:
# # #                 suggestion = suggest_best_slot(parsed)
# # #                 st.session_state.pending_parsed_data = parsed
# # #                 st.session_state.current_suggestion = suggestion

# # #                 if not suggestion.get("success"):
# # #                     err = f"❌ {suggestion.get('message','Unable to find slots')}"
# # #                     st.markdown(err)
# # #                     st.session_state.messages.append({"role":"assistant","content":err})
# # #                 else:
# # #                     if suggestion.get("conflict"):
# # #                         conflict = suggestion["conflict"]
# # #                         response = f"""⚠️ **Event Conflict Detected!**

# # # 🚫 **Existing Event at Requested Time:**
# # # - **Event Name:** {conflict.get('summary','Untitled')}
# # # - **Time:** {conflict['start'].strftime('%a, %b %d at %I:%M %p')} - {conflict['end'].strftime('%I:%M %p')}

# # # ✅ **Available Alternative Slots:**
# # # - **Title:** {parsed.get('title')}
# # # - **Duration:** {parsed.get('duration_minutes')} minutes

# # # 👇 Click on any available time slot below.
# # # """
# # #                         st.markdown(response)
# # #                         st.session_state.messages.append({"role":"assistant","content":response})
# # #                         st.session_state.pending_slot = None
# # #                         st.session_state.selected_alternative = None
# # #                     else:
# # #                         slot = suggestion["slot"]
# # #                         st.session_state.pending_slot = slot
# # #                         formatted = format_slot_for_display(slot)
# # #                         response = f"""✅ **Found slot**

# # # 📅 **{parsed.get('title')}**
# # # - **When:** {formatted['full_display']}
# # # - **Duration:** {parsed.get('duration_minutes')} minutes

# # # Click 'Confirm & Create Event' to book.
# # # """
# # #                         st.markdown(response)
# # #                         st.session_state.messages.append({"role":"assistant","content":response})

# # # # -------------------------
# # # # Pending confirm message
# # # # -------------------------
# # # if st.session_state._pending_confirm_msg:
# # #     msg = st.session_state._pending_confirm_msg
# # #     last = st.session_state.messages[-1]["content"] if st.session_state.messages else None
# # #     if last != msg:
# # #         st.session_state.messages.append({"role":"assistant","content":msg})
# # #     st.session_state._pending_confirm_msg = None

# # # # -------------------------
# # # # Alternative slot buttons
# # # # -------------------------
# # # if st.session_state.current_suggestion and st.session_state.current_suggestion.get("alternatives"):
# # #     suggestion = st.session_state.current_suggestion
# # #     alts = suggestion.get("alternatives", [])
# # #     if alts:
# # #         st.markdown("---")
# # #         st.markdown("### 📅 Available Time Slots")
# # #         cols = st.columns(min(3, len(alts)))
# # #         for idx, slot in enumerate(alts):
# # #             formatted = format_slot_for_display(slot)
# # #             btn_key = f"alt_{idx}_{slot['start'].isoformat()}"
# # #             clicked = cols[idx % 3].button(f"📅 {formatted['date']}\n⏰ {formatted['time_range']}", key=btn_key, use_container_width=True)
# # #             if clicked:
# # #                 st.session_state.pending_slot = slot
# # #                 st.session_state.selected_alternative = idx
# # #                 st.session_state._pending_confirm_msg = f"✅ Selected: **{formatted['full_display']}**\n\nClick 'Confirm & Create Event' below to book this slot."
# # #                 st.rerun()

# # # # -------------------------
# # # # Confirmation block
# # # # -------------------------
# # # if st.session_state.pending_slot:
# # #     st.markdown("---")
# # #     col1, col2, col3 = st.columns([1, 2, 1])
# # #     with col2:
# # #         confirm = st.button("✅ Confirm & Create Event", type="primary", use_container_width=True, key="confirm_create")
# # #         cancel = st.button("❌ Cancel", use_container_width=True, key="cancel_create")

# # #         if confirm:
# # #             with st.spinner("📅 Creating event..."):
# # #                 if st.session_state.event_created:
# # #                     st.info("Event already created in this session.")
# # #                 else:
# # #                     try:
# # #                         slot = st.session_state.pending_slot
# # #                         parsed = st.session_state.pending_parsed_data
# # #                         created = create_event(
# # #                             summary=parsed.get("title","Meeting"),
# # #                             start_datetime=slot["start"],
# # #                             end_datetime=slot["end"],
# # #                             description=parsed.get("description","Created by AI Meeting Scheduler Agent"),
# # #                             attendees=parsed.get("attendees",[])
# # #                         )
# # #                         if created:
# # #                             formatted = format_slot_for_display(slot)
# # #                             event_link = created.get('htmlLink', '#')
# # #                             success = f"""🎉 **Event Created Successfully!**

# # # 📅 **{parsed.get('title','Meeting')}**
# # # - **Time:** {formatted['full_display']}

# # # [📱 View in Google Calendar]({event_link})
# # # """
# # #                             st.session_state.messages.append({"role":"assistant","content":success})
# # #                             st.session_state.pending_slot = None
# # #                             st.session_state.pending_parsed_data = None
# # #                             st.session_state.current_suggestion = None
# # #                             st.session_state.selected_alternative = None
# # #                             st.session_state.event_created = True
# # #                             st.success("✅ Event created successfully!")
# # #                             st.balloons()
# # #                             st.rerun()
# # #                         else:
# # #                             err = "❌ Failed to create event. Try again."
# # #                             st.session_state.messages.append({"role":"assistant","content":err})
# # #                             st.error(err)
# # #                     except Exception as e:
# # #                         err = f"❌ Error creating event: {e}"
# # #                         st.session_state.messages.append({"role":"assistant","content":err})
# # #                         st.error(err)

# # #         if cancel:
# # #             st.session_state.pending_slot = None
# # #             st.session_state.pending_parsed_data = None
# # #             st.session_state.current_suggestion = None
# # #             st.session_state.selected_alternative = None
# # #             st.session_state._pending_confirm_msg = None
# # #             cancel_msg = "❌ Meeting request cancelled. Feel free to make a new request!"
# # #             last = st.session_state.messages[-1]["content"] if st.session_state.messages else None
# # #             if last != cancel_msg:
# # #                 st.session_state.messages.append({"role":"assistant","content":cancel_msg})
# # #             st.rerun()

# # # # Footer
# # # st.markdown("---")
# # # st.markdown('<div style="text-align:center;color:#666;font-size:0.9rem;">Powered by Google Calendar API | Built with Streamlit</div>', unsafe_allow_html=True)


































# # #everything working here..changing ui a bit
# # import streamlit as st
# # from datetime import datetime, timedelta, date
# # import pytz
# # import calendar as cal_module

# # from scheduler.gpt_parser import parse_meeting_request, parse_datetime_from_parsed_data
# # from scheduler.scheduler_logic import suggest_best_slot, format_slot_for_display
# # from scheduler.google_calendar import create_event, get_upcoming_events




# # import streamlit.components.v1 as components

# # # Inject mic + speech recognition JS
# # def stt_component():
# #     component_html = """
# #     <script>
# #     // Create global speech recognition object
# #     if (!window.sttSetupDone) {
# #         window.sttSetupDone = true;
        
# #         const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
# #         let recognition = null;

# #         if (SpeechRecognition) {
# #             recognition = new SpeechRecognition();
# #             recognition.continuous = false;
# #             recognition.interimResults = false;
# #             recognition.lang = "en-US";

# # recognition.onresult = function(event) {
# #                 const text = event.results[0][0].transcript;
                
# #                 // DEBUG: Log what was transcribed
# #                 console.log("🎤 Transcribed text:", text);
# #                 console.log("🎤 Text length:", text.length);
# #                 console.log("🎤 Text characters:", Array.from(text).map(c => c.charCodeAt(0)));
                
# #                 const inputBox = window.parent.document.querySelector('textarea[data-testid="stChatInputTextArea"]');

# #                 if (inputBox) {
# #                     // Set the value using React's internal setter
# #                     const nativeInputValueSetter = Object.getOwnPropertyDescriptor(
# #                         window.HTMLTextAreaElement.prototype, 
# #                         "value"
# #                     ).set;
# #                     nativeInputValueSetter.call(inputBox, text);
                    
# #                     // Trigger multiple events to ensure Streamlit recognizes the change
# #                     inputBox.dispatchEvent(new Event("input", {bubbles: true}));
# #                     inputBox.dispatchEvent(new Event("change", {bubbles: true}));
                    
# #                     // Focus the input so user can press Enter to send
# #                     inputBox.focus();
# #                 }
# #             };

# #             recognition.onerror = function(event) {
# #                 console.log("STT Error:", event.error);
# #             };
# #         }

# #             // Add mic button next to Streamlit chat input
# #         function addMicButton() {
# #             // NEW Streamlit chat input container selector
# #             const inputRow = window.parent.document.querySelector('div[data-testid="stChatInput"]');

# #             if (!inputRow) return;

# #             // Prevent duplicate buttons
# #             const alreadyExists = window.parent.document.querySelector("#mic-btn");
# # if (alreadyExists) return;


# #             // Create mic button
# #             const btn = document.createElement("button");
# #             btn.id = "mic-btn";
# #             btn.innerHTML = "🎤";
# #             btn.style.marginLeft = "6px";
# #             btn.style.padding = "4px 10px";
# #             btn.style.fontSize = "18px";
# #             btn.style.borderRadius = "6px";
# #             btn.style.cursor = "pointer";
# #             btn.style.border = "1px solid #ccc";
# #             btn.style.background = "white";

# #             let listening = false;

# # btn.onclick = function () {
# #     if (!recognition) return;

# #     if (!listening) {
# #         recognition.start();
# #         listening = true;
# #         btn.innerHTML = "🛑";
# #         btn.style.background = "#ffcccc";
# #     } else {
# #         recognition.stop();
# #         listening = false;
# #         btn.innerHTML = "🎤";
# #         btn.style.background = "white";
# #     }
# # };


# #             // Append mic button AFTER the text area
# #             inputRow.appendChild(btn);
# #         }


# #         setInterval(addMicButton, 800);
# #     }
# #     </script>
# #     """
# #     components.html(component_html, height=0, width=0)





# # # -------------------------
# # # Page + session init
# # # -------------------------
# # st.set_page_config(page_title="AI Meeting Scheduler", page_icon="📅", layout="wide")

# # LOCAL_TZ = pytz.timezone("Asia/Kolkata")

# # # Initialize ALL session state at the very beginning
# # today = date.today()
# # if "current_month" not in st.session_state:
# #     st.session_state.current_month = today.month
# # if "current_year" not in st.session_state:
# #     st.session_state.current_year = today.year
# # if "messages" not in st.session_state:
# #     st.session_state.messages = []
# # if "pending_slot" not in st.session_state:
# #     st.session_state.pending_slot = None
# # if "pending_parsed_data" not in st.session_state:
# #     st.session_state.pending_parsed_data = None
# # if "current_suggestion" not in st.session_state:
# #     st.session_state.current_suggestion = None
# # if "selected_alternative" not in st.session_state:
# #     st.session_state.selected_alternative = None
# # if "event_created" not in st.session_state:
# #     st.session_state.event_created = False
# # if "_pending_confirm_msg" not in st.session_state:
# #     st.session_state._pending_confirm_msg = None

# # # -------------------------
# # # CALLBACK FUNCTIONS for month navigation
# # # -------------------------
# # def go_prev_month():
# #     if st.session_state.current_month == 1:
# #         st.session_state.current_month = 12
# #         st.session_state.current_year -= 1
# #     else:
# #         st.session_state.current_month -= 1

# # def go_next_month():
# #     if st.session_state.current_month == 12:
# #         st.session_state.current_month = 1
# #         st.session_state.current_year += 1
# #     else:
# #         st.session_state.current_month += 1

# # # -------------------------
# # # Helper function: Format datetime properly
# # # -------------------------
# # def format_event_time(event_time_str):
# #     """Convert ISO datetime string to readable format"""
# #     try:
# #         if 'T' in event_time_str:
# #             dt = datetime.fromisoformat(event_time_str.replace('Z', '+00:00'))
# #             dt_local = dt.astimezone(LOCAL_TZ)
# #             return dt_local.strftime('%a, %b %d at %I:%M %p')
# #         else:
# #             dt = datetime.strptime(event_time_str, '%Y-%m-%d')
# #             return dt.strftime('%a, %b %d (All day)')
# #     except:
# #         return event_time_str

# # def get_events_for_date(target_date):
# #     """Get all events for a specific date"""
# #     try:
# #         from scheduler.google_calendar import get_calendar_service
# #         import pytz
        
# #         service = get_calendar_service()
        
# #         start_of_day = LOCAL_TZ.localize(
# #             datetime.combine(target_date, datetime.min.time())
# #         )
# #         end_of_day = LOCAL_TZ.localize(
# #             datetime.combine(target_date, datetime.max.time())
# #         )
        
# #         time_min = start_of_day.astimezone(pytz.UTC).isoformat()
# #         time_max = end_of_day.astimezone(pytz.UTC).isoformat()
        
# #         events_result = service.events().list(
# #             calendarId='primary',
# #             timeMin=time_min,
# #             timeMax=time_max,
# #             singleEvents=True,
# #             orderBy='startTime'
# #         ).execute()
        
# #         events = events_result.get('items', [])
        
# #         formatted_events = []
# #         for event in events:
# #             start = event['start'].get('dateTime', event['start'].get('date'))
# #             end = event['end'].get('dateTime', event['end'].get('date'))
            
# #             if 'T' in start:
# #                 start_dt = datetime.fromisoformat(start.replace('Z', '+00:00')).astimezone(LOCAL_TZ)
# #                 end_dt = datetime.fromisoformat(end.replace('Z', '+00:00')).astimezone(LOCAL_TZ)
# #                 time_str = f"{start_dt.strftime('%I:%M %p')} - {end_dt.strftime('%I:%M %p')}"
# #             else:
# #                 time_str = "All day"
            
# #             formatted_events.append({
# #                 'summary': event.get('summary', 'Untitled'),
# #                 'time': time_str,
# #                 'description': event.get('description', '')
# #             })
        
# #         return formatted_events
# #     except Exception as e:
# #         return []

# # # -------------------------
# # # UI CSS
# # # -------------------------
# # st.markdown(
# #     """
# # <style>
# #     /* Global Dark Theme - Fixed blur issue */
# #     .stApp {
# #         background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%) !important;
# #         background-attachment: fixed !important;
# #     }
    
# #     /* Main content area - remove any conflicting backgrounds */
# #     .main .block-container {
# #         background: transparent !important;
# #     }
    
# #     /* Sidebar Glassmorphism - NO BLUR */
# #     section[data-testid="stSidebar"] {
# #         background: rgba(255, 255, 255, 0.05) !important;
# #         backdrop-filter: none !important;
# #         border-right: 1px solid rgba(255, 255, 255, 0.1) !important;
# #     }
    
# #     section[data-testid="stSidebar"] * {
# #         color: #e0e0e0 !important;
# #     }
    
# #     /* Headers */
# #     .main-header { 
# #         font-size: 2.5rem; 
# #         font-weight: 700; 
# #         background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
# #         -webkit-background-clip: text;
# #         -webkit-text-fill-color: transparent;
# #         text-align: center; 
# #         margin-bottom: 8px;
# #         text-shadow: 0 0 30px rgba(102, 126, 234, 0.3);
# #     }
    
# #     .sub-header { 
# #         font-size: 1.1rem; 
# #         color: #b0b0b0; 
# #         text-align: center; 
# #         margin-bottom: 20px;
# #         font-weight: 300;
# #     }
    
# #     /* Calendar Grid - Glassmorphism */
# #     .calendar-grid { 
# #         display: grid; 
# #         grid-template-columns: repeat(7, 1fr); 
# #         gap: 6px; 
# #         margin: 12px 0;
# #         padding: 15px;
# #         background: rgba(255, 255, 255, 0.03);
# #         backdrop-filter: blur(10px);
# #         border-radius: 16px;
# #         border: 1px solid rgba(255, 255, 255, 0.1);
# #     }
    
# #     .calendar-day { 
# #         aspect-ratio: 1; 
# #         display: flex; 
# #         align-items: center; 
# #         justify-content: center; 
# #         background: rgba(255, 255, 255, 0.05); 
# #         border-radius: 10px; 
# #         font-size: 0.9rem; 
# #         font-weight: 500;
# #         border: 1px solid rgba(255, 255, 255, 0.05);
# #         transition: all 0.3s ease;
# #     }
    
# #     .calendar-day:hover {
# #         background: rgba(102, 126, 234, 0.2);
# #         transform: scale(1.05);
# #     }
    
# #     .calendar-header { 
# #         font-weight: 700; 
# #         background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
# #         color: white;
# #         border: none;
# #     }
    
# #     .calendar-today { 
# #         background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
# #         color: white; 
# #         font-weight: 700;
# #         box-shadow: 0 4px 15px rgba(245, 87, 108, 0.4);
# #     }
    
# #  /* Blue Glass Section - View Events */
# # # .blue-glass-section {
# # #     background: rgba(102, 126, 234, 0.18) !important;
# # #     backdrop-filter: blur(14px) !important;
# # #     -webkit-backdrop-filter: blur(14px) !important;

# # #     border-radius: 16px !important;
# # #     padding: 18px 22px !important;
# # #     margin: 18px 0 !important;

# # #     border: 1.2px solid rgba(102, 126, 234, 0.5) !important;
# # #     box-shadow: 0 4px 20px rgba(102, 126, 234, 0.35) !important;
# # # }

    
# #     /* Purple Glass Section - Upcoming Events */
# #    .purple-glass-section {
# #     background: rgba(118, 75, 162, 0.22) !important;   /* darker glass */
# #     backdrop-filter: blur(12px) !important;
# #     -webkit-backdrop-filter: blur(12px) !important;

# #     border-radius: 16px !important;  /* slightly smaller corners */
# #     padding: 16px 20px !important;   /* thinner padding */
# #     margin: 16px 0 !important;

# #     border: 1.2px solid rgba(118, 75, 162, 0.55) !important; /* thinner border but darker */

# #     box-shadow: 0 4px 18px rgba(118, 75, 162, 0.35) !important; /* smaller but darker shadow */
# # }

    
# #     /* Event Cards */
# #     .event-card {
# #         background: rgba(255, 255, 255, 0.05);
# #         backdrop-filter: blur(5px);
# #         border-radius: 12px;
# #         padding: 15px;
# #         margin: 10px 0;
# #         border-left: 4px solid #667eea;
# #         transition: all 0.3s ease;
# #     }
    
# #     .event-card:hover {
# #         background: rgba(255, 255, 255, 0.08);
# #         transform: translateX(5px);
# #         box-shadow: 0 4px 20px rgba(102, 126, 234, 0.3);
# #     }
    
# #     /* Buttons - Glassmorphism */
# #     .stButton > button {
# #         background: rgba(255, 255, 255, 0.1) !important;
# #         backdrop-filter: blur(10px) !important;
# #         border: 1px solid rgba(255, 255, 255, 0.2) !important;
# #         border-radius: 12px !important;
# #         color: #e0e0e0 !important;
# #         font-weight: 500 !important;
# #         transition: all 0.3s ease !important;
# #     }
    
# #     .stButton > button:hover {
# #         background: rgba(102, 126, 234, 0.3) !important;
# #         border-color: rgba(102, 126, 234, 0.5) !important;
# #         transform: translateY(-2px);
# #         box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4) !important;
# #     }
    
# #     /* Primary Button */
# #     .stButton > button[kind="primary"] {
# #         background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
# #         border: none !important;
# #         color: white !important;
# #         font-weight: 600 !important;
# #     }
    
# #     .stButton > button[kind="primary"]:hover {
# #         background: linear-gradient(135deg, #764ba2 0%, #667eea 100%) !important;
# #         box-shadow: 0 6px 25px rgba(102, 126, 234, 0.6) !important;
# #     }
    
# #     /* Input Fields - BLACK TEXT */
# #     .stTextInput > div > div > input {
# #         background: rgba(255, 255, 255, 0.9) !important;
# #         backdrop-filter: blur(10px) !important;
# #         border: 1px solid rgba(255, 255, 255, 0.2) !important;
# #         border-radius: 12px !important;
# #         color: #000000 !important;
# #         font-weight: 500 !important;
# #     }
    
# #     .stTextInput > div > div > input::placeholder {
# #         color: rgba(0, 0, 0, 0.5) !important;
# #     }
    
# #     /* Chat Messages */
# #     .stChatMessage {
# #         background: rgba(255, 255, 255, 0.05) !important;
# #         backdrop-filter: blur(10px) !important;
# #         border: 1px solid rgba(255, 255, 255, 0.1) !important;
# #         border-radius: 16px !important;
# #     }
    
# #     /* Markdown in dark mode */
# #     .stMarkdown {
# #         color: #e0e0e0 !important;
# #     }
    
# #     /* Dividers */
# #     hr {
# #         border-color: rgba(255, 255, 255, 0.1) !important;
# #         margin: 20px 0 !important;
# #     }
    
# #     /* Section Headers */
# #     h3 {
# #         color: #b0b0b0 !important;
# #         font-weight: 600 !important;
# #         margin-top: 15px !important;
# #     }
    
# #     /* Info/Warning boxes */
# #     .stInfo, .stWarning, .stSuccess {
# #         background: rgba(255, 255, 255, 0.05) !important;
# #         backdrop-filter: blur(10px) !important;
# #         border-radius: 12px !important;
# #         border-left: 4px solid #667eea !important;
# #     }
# # </style>
# # """,
# #     unsafe_allow_html=True,
# # )

# # # -------------------------
# # # Sidebar (calendar + upcoming)
# # # -------------------------
# # with st.sidebar:
# #     st.markdown("### 📅 Meeting Scheduler")
# #     st.markdown("---")

# #     # Month navigation with CALLBACKS
# #     col1, col2, col3 = st.columns([1, 2, 1])
    
# #     col1.button("◀", key="prev_month", on_click=go_prev_month, use_container_width=True)
# #     col2.markdown(f"<div style='text-align:center; padding-top:8px;'><strong>{cal_module.month_name[st.session_state.current_month]} {st.session_state.current_year}</strong></div>", unsafe_allow_html=True)
# #     col3.button("▶", key="next_month", on_click=go_next_month, use_container_width=True)

# #     # Calendar display
# #     cal = cal_module.monthcalendar(st.session_state.current_year, st.session_state.current_month)
# #     calendar_html = '<div class="calendar-grid">'
    
# #     for day in ['Mo','Tu','We','Th','Fr','Sa','Su']:
# #         calendar_html += f'<div class="calendar-day calendar-header">{day}</div>'
    
# #     for week in cal:
# #         for d in week:
# #             if d == 0:
# #                 calendar_html += '<div class="calendar-day"></div>'
# #             else:
# #                 is_today = (d == today.day and 
# #                            st.session_state.current_month == today.month and 
# #                            st.session_state.current_year == today.year)
# #                 css = "calendar-today" if is_today else ""
# #                 calendar_html += f'<div class="calendar-day {css}">{d}</div>'
    
# #     calendar_html += '</div>'
# #     st.markdown(calendar_html, unsafe_allow_html=True)
    
# #     # Date selector - BLUE GLASS SECTION
# #     st.markdown("---")
# #     st.markdown('<div class="blue-glass-section">', unsafe_allow_html=True)
# #     st.markdown("**📅 View Events for Date:**")
    
# #     date_input = st.text_input(
# #         "Type date (DD/MM/YYYY)",
# #         placeholder="28/11/2025",
# #         key="manual_date_input",
# #         help="Enter date in DD/MM/YYYY format"
# #     )
    
# #     if st.button("📅 View Events", use_container_width=True, key="view_events_btn"):
# #         selected_date = None
        
# #         if date_input.strip():
# #             try:
# #                 parts = date_input.strip().split('/')
# #                 if len(parts) == 3:
# #                     day, month, year = int(parts[0]), int(parts[1]), int(parts[2])
# #                     selected_date = date(year, month, day)
# #             except:
# #                 st.error("❌ Invalid format! Use DD/MM/YYYY (e.g., 28/11/2025)")
        
# #         if selected_date:
# #             events = get_events_for_date(selected_date)
            
# #             st.markdown(f"**📆 {selected_date.strftime('%A, %B %d, %Y')}**")
# #             st.markdown("---")
            
# #             if events:
# #                 for event in events:
# #                     st.markdown(f"### 🕐 {event['time']}")
# #                     st.markdown(f"**{event['summary']}**")
# #                     if event.get('description'):
# #                         st.caption(event['description'])
# #                     st.markdown("---")
# #             else:
# #                 st.info(f"✨ No events on {selected_date.strftime('%B %d')}")
# #         else:
# #             st.warning("⚠️ Please enter a date in DD/MM/YYYY format")
    
# #     st.markdown('</div>', unsafe_allow_html=True)  # Close blue glass section

# #     st.markdown("---")
# #     st.markdown('<div class="purple-glass-section">', unsafe_allow_html=True)
# #     st.markdown("### 📋 Upcoming Events")
# #     try:
# #         events = get_upcoming_events(5)
# #         if events:
# #             for ev in events:
# #                 start = ev['start'].get('dateTime', ev['start'].get('date'))
# #                 formatted_time = format_event_time(start)
# #                 st.markdown(f"**{ev.get('summary','Untitled')}**")
# #                 st.caption(formatted_time)
# #                 st.markdown("---")
# #         else:
# #             st.info("No upcoming events")
# #     except:
# #         st.warning("Could not load events")
    
# #     st.markdown('</div>', unsafe_allow_html=True)  # Close purple glass section

# #     st.markdown("---")
# #     st.markdown("### 💡 How to use")
# #     st.markdown("- **Type date** in DD/MM/YYYY format\n- Click 'View Events'\n- Type meeting requests below")
    
# #     if st.button("🗑️ Clear chat", use_container_width=True):
# #         st.session_state.messages = []
# #         st.session_state.pending_slot = None
# #         st.session_state.pending_parsed_data = None
# #         st.session_state.current_suggestion = None
# #         st.session_state.selected_alternative = None
# #         st.session_state._pending_confirm_msg = None
# #         st.rerun()

# # # -------------------------
# # # Main content header
# # # -------------------------
# # st.markdown('<div class="main-header">🤖 AI Meeting Scheduler Agent</div>', unsafe_allow_html=True)
# # st.markdown('<div class="sub-header">Schedule meetings using natural language</div>', unsafe_allow_html=True)

# # # -------------------------
# # # Render chat messages
# # # -------------------------
# # for msg in st.session_state.messages:
# #     with st.chat_message(msg["role"]):
# #         st.markdown(msg["content"], unsafe_allow_html=True)

# # # -------------------------
# # # Chat input -> parse -> suggest
# # # -------------------------


# # # Inject STT microphone functionality
# # stt_component()

# # user_input = st.chat_input("Type your meeting request here... (e.g., 'Schedule meeting tomorrow at 3pm')")

# # if user_input:
# #     st.session_state.messages.append({"role":"user","content":user_input})
# #     with st.chat_message("user"):
# #         st.markdown(user_input)

# #     with st.chat_message("assistant"):
# #         with st.spinner("🔍 Analyzing your request..."):
# #             parsed = parse_meeting_request(user_input)
# #             if not parsed:
# #                 err = "❌ Couldn't understand. Try: 'Schedule meeting tomorrow at 3pm for 30 minutes'"
# #                 st.markdown(err)
# #                 st.session_state.messages.append({"role":"assistant","content":err})
# #             else:
# #                 suggestion = suggest_best_slot(parsed)
# #                 st.session_state.pending_parsed_data = parsed
# #                 st.session_state.current_suggestion = suggestion

# #                 if not suggestion.get("success"):
# #                     err = f"❌ {suggestion.get('message','Unable to find slots')}"
# #                     st.markdown(err)
# #                     st.session_state.messages.append({"role":"assistant","content":err})
# #                 else:
# #                     if suggestion.get("conflict"):
# #                         conflict = suggestion["conflict"]
# #                         response = f"""⚠️ **Event Conflict Detected!**

# # 🚫 **Existing Event at Requested Time:**
# # - **Event Name:** {conflict.get('summary','Untitled')}
# # - **Time:** {conflict['start'].strftime('%a, %b %d at %I:%M %p')} - {conflict['end'].strftime('%I:%M %p')}

# # ✅ **Available Alternative Slots:**
# # - **Title:** {parsed.get('title')}
# # - **Duration:** {parsed.get('duration_minutes')} minutes

# # 👇 Click on any available time slot below.
# # """
# #                         st.markdown(response)
# #                         st.session_state.messages.append({"role":"assistant","content":response})
# #                         st.session_state.pending_slot = None
# #                         st.session_state.selected_alternative = None
# #                     else:
# #                         slot = suggestion["slot"]
# #                         st.session_state.pending_slot = slot
# #                         formatted = format_slot_for_display(slot)
# #                         response = f"""✅ **Found slot**

# # 📅 **{parsed.get('title')}**
# # - **When:** {formatted['full_display']}
# # - **Duration:** {parsed.get('duration_minutes')} minutes

# # Click 'Confirm & Create Event' to book.
# # """
# #                         st.markdown(response)
# #                         st.session_state.messages.append({"role":"assistant","content":response})

# # # -------------------------
# # # Pending confirm message
# # # -------------------------
# # if st.session_state._pending_confirm_msg:
# #     msg = st.session_state._pending_confirm_msg
# #     last = st.session_state.messages[-1]["content"] if st.session_state.messages else None
# #     if last != msg:
# #         st.session_state.messages.append({"role":"assistant","content":msg})
# #     st.session_state._pending_confirm_msg = None

# # # -------------------------
# # # Alternative slot buttons
# # # -------------------------
# # if st.session_state.current_suggestion and st.session_state.current_suggestion.get("alternatives"):
# #     suggestion = st.session_state.current_suggestion
# #     alts = suggestion.get("alternatives", [])
# #     if alts:
# #         st.markdown("---")
# #         st.markdown("### 📅 Available Time Slots")
# #         cols = st.columns(min(3, len(alts)))
# #         for idx, slot in enumerate(alts):
# #             formatted = format_slot_for_display(slot)
# #             btn_key = f"alt_{idx}_{slot['start'].isoformat()}"
# #             clicked = cols[idx % 3].button(f"📅 {formatted['date']}\n⏰ {formatted['time_range']}", key=btn_key, use_container_width=True)
# #             if clicked:
# #                 st.session_state.pending_slot = slot
# #                 st.session_state.selected_alternative = idx
# #                 st.session_state._pending_confirm_msg = f"✅ Selected: **{formatted['full_display']}**\n\nClick 'Confirm & Create Event' below to book this slot."
# #                 st.rerun()

# # # -------------------------
# # # Confirmation block
# # # -------------------------
# # if st.session_state.pending_slot:
# #     st.markdown("---")
# #     col1, col2, col3 = st.columns([1, 2, 1])
# #     with col2:
# #         confirm = st.button("✅ Confirm & Create Event", type="primary", use_container_width=True, key="confirm_create")
# #         cancel = st.button("❌ Cancel", use_container_width=True, key="cancel_create")

# #         if confirm:
# #             with st.spinner("📅 Creating event..."):
# #                 if st.session_state.event_created:
# #                     st.info("Event already created in this session.")
# #                 else:
# #                     try:
# #                         slot = st.session_state.pending_slot
# #                         parsed = st.session_state.pending_parsed_data
# #                         created = create_event(
# #                             summary=parsed.get("title","Meeting"),
# #                             start_datetime=slot["start"],
# #                             end_datetime=slot["end"],
# #                             description=parsed.get("description","Created by AI Meeting Scheduler Agent"),
# #                             attendees=parsed.get("attendees",[])
# #                         )
# #                         if created:
# #                             formatted = format_slot_for_display(slot)
# #                             event_link = created.get('htmlLink', '#')
# #                             success = f"""🎉 **Event Created Successfully!**

# # 📅 **{parsed.get('title','Meeting')}**
# # - **Time:** {formatted['full_display']}

# # [📱 View in Google Calendar]({event_link})
# # """
# #                             st.session_state.messages.append({"role":"assistant","content":success})
# #                             st.session_state.pending_slot = None
# #                             st.session_state.pending_parsed_data = None
# #                             st.session_state.current_suggestion = None
# #                             st.session_state.selected_alternative = None
# #                             st.session_state.event_created = True
# #                             st.success("✅ Event created successfully!")
# #                             st.balloons()
# #                             st.rerun()
# #                         else:
# #                             err = "❌ Failed to create event. Try again."
# #                             st.session_state.messages.append({"role":"assistant","content":err})
# #                             st.error(err)
# #                     except Exception as e:
# #                         err = f"❌ Error creating event: {e}"
# #                         st.session_state.messages.append({"role":"assistant","content":err})
# #                         st.error(err)

# #         if cancel:
# #             st.session_state.pending_slot = None
# #             st.session_state.pending_parsed_data = None
# #             st.session_state.current_suggestion = None
# #             st.session_state.selected_alternative = None
# #             st.session_state._pending_confirm_msg = None
# #             cancel_msg = "❌ Meeting request cancelled. Feel free to make a new request!"
# #             last = st.session_state.messages[-1]["content"] if st.session_state.messages else None
# #             if last != cancel_msg:
# #                 st.session_state.messages.append({"role":"assistant","content":cancel_msg})
# #             st.rerun()

# # # Footer
# # st.markdown("---")
# # st.markdown('<div style="text-align:center;color:#666;font-size:0.9rem;">Powered by Google Calendar API | Built with Streamlit</div>', unsafe_allow_html=True)







































# #fixing multiple issues here..

# import streamlit as st
# from datetime import datetime, timedelta, date
# import pytz
# import calendar as cal_module

# from scheduler.gpt_parser import parse_meeting_request, parse_datetime_from_parsed_data
# from scheduler.scheduler_logic import suggest_best_slot, format_slot_for_display
# from scheduler.google_calendar import create_event, get_upcoming_events

# import streamlit.components.v1 as components

# # -------------------------
# # FIXED: Speech-to-Text Component
# # -------------------------
# def stt_component():
#     component_html = """
#     <script>
#     (function() {
#         const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
#         if (!SpeechRecognition) {
#             console.error("Speech recognition not supported");
#             return;
#         }

#         let recognition = null;
#         let isListening = false;
#         let micButton = null;

#         function createRecognition() {
#             recognition = new SpeechRecognition();
#             recognition.continuous = false;
#             recognition.interimResults = false;
#             recognition.lang = "en-US";
            
#             recognition.onresult = function(event) {
#                 const text = event.results[0][0].transcript;
#                 console.log("🎤 Transcribed:", text);
                
#                 const inputBox = window.parent.document.querySelector('textarea[data-testid="stChatInputTextArea"]');
                
#                 if (inputBox) {
#                     const nativeInputValueSetter = Object.getOwnPropertyDescriptor(
#                         window.HTMLTextAreaElement.prototype, 
#                         "value"
#                     ).set;
#                     nativeInputValueSetter.call(inputBox, text);
                    
#                     inputBox.dispatchEvent(new Event("input", {bubbles: true}));
#                     inputBox.dispatchEvent(new Event("change", {bubbles: true}));
#                     inputBox.focus();
#                 }
                
#                 resetButton();
#             };

#             recognition.onerror = function(event) {
#                 console.error("STT Error:", event.error);
#                 resetButton();
#             };

#             recognition.onend = function() {
#                 resetButton();
#             };
#         }

#         function resetButton() {
#             isListening = false;
#             if (micButton) {
#                 micButton.innerHTML = "🎤";
#                 micButton.style.background = "linear-gradient(135deg, #667eea 0%, #764ba2 100%)";
#                 micButton.style.color = "white";
#             }
#         }

#         function addMicButton() {
#             const inputRow = window.parent.document.querySelector('div[data-testid="stChatInput"]');
#             if (!inputRow) return;

#             micButton = window.parent.document.querySelector("#mic-btn");
#             if (micButton) return;

#             micButton = window.parent.document.createElement("button");
#             micButton.id = "mic-btn";
#             micButton.innerHTML = "🎤";
#             micButton.style.marginLeft = "8px";
#             micButton.style.padding = "8px 12px";
#             micButton.style.fontSize = "20px";
#             micButton.style.borderRadius = "8px";
#             micButton.style.cursor = "pointer";
#             micButton.style.border = "none";
#             micButton.style.background = "linear-gradient(135deg, #667eea 0%, #764ba2 100%)";
#             micButton.style.color = "white";
#             micButton.style.transition = "all 0.3s ease";
#             micButton.style.boxShadow = "0 2px 8px rgba(102, 126, 234, 0.4)";

#             micButton.onmouseover = function() {
#                 if (!isListening) {
#                     micButton.style.transform = "scale(1.1)";
#                     micButton.style.boxShadow = "0 4px 12px rgba(102, 126, 234, 0.6)";
#                 }
#             };

#             micButton.onmouseout = function() {
#                 micButton.style.transform = "scale(1)";
#                 micButton.style.boxShadow = "0 2px 8px rgba(102, 126, 234, 0.4)";
#             };

#             micButton.onclick = function() {
#                 if (!isListening) {
#                     try {
#                         createRecognition();
#                         recognition.start();
#                         isListening = true;
#                         micButton.innerHTML = "🛑";
#                         micButton.style.background = "linear-gradient(135deg, #ff6b6b 0%, #ee5a6f 100%)";
#                         micButton.style.animation = "pulse 1.5s infinite";
#                     } catch (e) {
#                         console.error("Failed to start recognition:", e);
#                         resetButton();
#                     }
#                 } else {
#                     if (recognition) {
#                         recognition.stop();
#                     }
#                     resetButton();
#                 }
#             };

#             inputRow.appendChild(micButton);
            
#             // Add pulse animation
#             const style = window.parent.document.createElement('style');
#             style.textContent = `
#                 @keyframes pulse {
#                     0%, 100% { opacity: 1; }
#                     50% { opacity: 0.7; }
#                 }
#             `;
#             window.parent.document.head.appendChild(style);
#         }

#         addMicButton();
#         setInterval(addMicButton, 800);
#     })();
#     </script>
#     """
#     components.html(component_html, height=0, width=0)

# # -------------------------
# # Page + session init
# # -------------------------
# st.set_page_config(page_title="AI Meeting Scheduler", page_icon="📅", layout="wide")

# LOCAL_TZ = pytz.timezone("Asia/Kolkata")

# # FIXED: Initialize ALL session state properly
# today = date.today()
# defaults = {
#     "current_month": today.month,
#     "current_year": today.year,
#     "messages": [],
#     "pending_slot": None,
#     "pending_parsed_data": None,
#     "current_suggestion": None,
#     "selected_alternative": None,
#     "event_created": False,
#     "_pending_confirm_msg": None,
#     "processing": False  # NEW: Prevent duplicate processing
# }

# for key, value in defaults.items():
#     if key not in st.session_state:
#         st.session_state[key] = value

# # -------------------------
# # CALLBACK FUNCTIONS for month navigation
# # -------------------------
# def go_prev_month():
#     if st.session_state.current_month == 1:
#         st.session_state.current_month = 12
#         st.session_state.current_year -= 1
#     else:
#         st.session_state.current_month -= 1

# def go_next_month():
#     if st.session_state.current_month == 12:
#         st.session_state.current_month = 1
#         st.session_state.current_year += 1
#     else:
#         st.session_state.current_month += 1

# # -------------------------
# # Helper functions
# # -------------------------
# def format_event_time(event_time_str):
#     """Convert ISO datetime string to readable format"""
#     try:
#         if 'T' in event_time_str:
#             dt = datetime.fromisoformat(event_time_str.replace('Z', '+00:00'))
#             dt_local = dt.astimezone(LOCAL_TZ)
#             return dt_local.strftime('%a, %b %d at %I:%M %p')
#         else:
#             dt = datetime.strptime(event_time_str, '%Y-%m-%d')
#             return dt.strftime('%a, %b %d (All day)')
#     except:
#         return event_time_str

# def get_events_for_date(target_date):
#     """Get all events for a specific date"""
#     try:
#         from scheduler.google_calendar import get_calendar_service
        
#         service = get_calendar_service()
        
#         start_of_day = LOCAL_TZ.localize(
#             datetime.combine(target_date, datetime.min.time())
#         )
#         end_of_day = LOCAL_TZ.localize(
#             datetime.combine(target_date, datetime.max.time())
#         )
        
#         time_min = start_of_day.astimezone(pytz.UTC).isoformat()
#         time_max = end_of_day.astimezone(pytz.UTC).isoformat()
        
#         events_result = service.events().list(
#             calendarId='primary',
#             timeMin=time_min,
#             timeMax=time_max,
#             singleEvents=True,
#             orderBy='startTime'
#         ).execute()
        
#         events = events_result.get('items', [])
        
#         formatted_events = []
#         for event in events:
#             start = event['start'].get('dateTime', event['start'].get('date'))
#             end = event['end'].get('dateTime', event['end'].get('date'))
            
#             if 'T' in start:
#                 start_dt = datetime.fromisoformat(start.replace('Z', '+00:00')).astimezone(LOCAL_TZ)
#                 end_dt = datetime.fromisoformat(end.replace('Z', '+00:00')).astimezone(LOCAL_TZ)
#                 time_str = f"{start_dt.strftime('%I:%M %p')} - {end_dt.strftime('%I:%M %p')}"
#             else:
#                 time_str = "All day"
            
#             formatted_events.append({
#                 'summary': event.get('summary', 'Untitled'),
#                 'time': time_str,
#                 'description': event.get('description', '')
#             })
        
#         return formatted_events
#     except Exception as e:
#         st.error(f"Error fetching events: {e}")
#         return []

# # -------------------------
# # UI CSS (same as before)
# # -------------------------
# st.markdown("""
# <style>
#     .stApp {
#         background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%) !important;
#         background-attachment: fixed !important;
#     }
    
#     .main .block-container {
#         background: transparent !important;
#     }
    
#     section[data-testid="stSidebar"] {
#         background: rgba(255, 255, 255, 0.05) !important;
#         backdrop-filter: none !important;
#         border-right: 1px solid rgba(255, 255, 255, 0.1) !important;
#     }
    
#     section[data-testid="stSidebar"] * {
#         color: #e0e0e0 !important;
#     }
    
#     .main-header { 
#         font-size: 2.5rem; 
#         font-weight: 700; 
#         background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
#         -webkit-background-clip: text;
#         -webkit-text-fill-color: transparent;
#         text-align: center; 
#         margin-bottom: 8px;
#         text-shadow: 0 0 30px rgba(102, 126, 234, 0.3);
#     }
    
#     .sub-header { 
#         font-size: 1.1rem; 
#         color: #b0b0b0; 
#         text-align: center; 
#         margin-bottom: 20px;
#         font-weight: 300;
#     }
    
#     .calendar-grid { 
#         display: grid; 
#         grid-template-columns: repeat(7, 1fr); 
#         gap: 6px; 
#         margin: 12px 0;
#         padding: 15px;
#         background: rgba(255, 255, 255, 0.03);
#         backdrop-filter: blur(10px);
#         border-radius: 16px;
#         border: 1px solid rgba(255, 255, 255, 0.1);
#     }
    
#     .calendar-day { 
#         aspect-ratio: 1; 
#         display: flex; 
#         align-items: center; 
#         justify-content: center; 
#         background: rgba(255, 255, 255, 0.05); 
#         border-radius: 10px; 
#         font-size: 0.9rem; 
#         font-weight: 500;
#         border: 1px solid rgba(255, 255, 255, 0.05);
#         transition: all 0.3s ease;
#     }
    
#     .calendar-day:hover {
#         background: rgba(102, 126, 234, 0.2);
#         transform: scale(1.05);
#     }
    
#     .calendar-header { 
#         font-weight: 700; 
#         background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
#         color: white;
#         border: none;
#     }
    
#     .calendar-today { 
#         background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
#         color: white; 
#         font-weight: 700;
#         box-shadow: 0 4px 15px rgba(245, 87, 108, 0.4);
#     }
    
#     .blue-glass-section {
#         background: rgba(102, 126, 234, 0.18) !important;
#         backdrop-filter: blur(14px) !important;
#         border-radius: 16px !important;
#         padding: 18px 22px !important;
#         margin: 18px 0 !important;
#         border: 1.2px solid rgba(102, 126, 234, 0.5) !important;
#         box-shadow: 0 4px 20px rgba(102, 126, 234, 0.35) !important;
#     }
    
#     .purple-glass-section {
#         background: rgba(118, 75, 162, 0.22) !important;
#         backdrop-filter: blur(12px) !important;
#         border-radius: 16px !important;
#         padding: 16px 20px !important;
#         margin: 16px 0 !important;
#         border: 1.2px solid rgba(118, 75, 162, 0.55) !important;
#         box-shadow: 0 4px 18px rgba(118, 75, 162, 0.35) !important;
#     }
    
#     .event-card {
#         background: rgba(255, 255, 255, 0.05);
#         backdrop-filter: blur(5px);
#         border-radius: 12px;
#         padding: 15px;
#         margin: 10px 0;
#         border-left: 4px solid #667eea;
#         transition: all 0.3s ease;
#     }
    
#     .event-card:hover {
#         background: rgba(255, 255, 255, 0.08);
#         transform: translateX(5px);
#         box-shadow: 0 4px 20px rgba(102, 126, 234, 0.3);
#     }
    
#     .stButton > button {
#         background: rgba(255, 255, 255, 0.1) !important;
#         backdrop-filter: blur(10px) !important;
#         border: 1px solid rgba(255, 255, 255, 0.2) !important;
#         border-radius: 12px !important;
#         color: #e0e0e0 !important;
#         font-weight: 500 !important;
#         transition: all 0.3s ease !important;
#     }
    
#     .stButton > button:hover {
#         background: rgba(102, 126, 234, 0.3) !important;
#         border-color: rgba(102, 126, 234, 0.5) !important;
#         transform: translateY(-2px);
#         box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4) !important;
#     }
    
#     .stButton > button[kind="primary"] {
#         background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
#         border: none !important;
#         color: white !important;
#         font-weight: 600 !important;
#     }
    
#     .stButton > button[kind="primary"]:hover {
#         background: linear-gradient(135deg, #764ba2 0%, #667eea 100%) !important;
#         box-shadow: 0 6px 25px rgba(102, 126, 234, 0.6) !important;
#     }
    
#     .stTextInput > div > div > input,
#     .stTextArea > div > div > textarea {
#         background: rgba(255, 255, 255, 0.9) !important;
#         backdrop-filter: blur(10px) !important;
#         border: 1px solid rgba(255, 255, 255, 0.2) !important;
#         border-radius: 12px !important;
#         color: #000000 !important;
#         font-weight: 500 !important;
#     }
    
#     .stTextInput > div > div > input::placeholder,
#     .stTextArea > div > div > textarea::placeholder {
#         color: rgba(0, 0, 0, 0.5) !important;
#     }
    
#     .stChatMessage {
#         background: rgba(255, 255, 255, 0.05) !important;
#         backdrop-filter: blur(10px) !important;
#         border: 1px solid rgba(255, 255, 255, 0.1) !important;
#         border-radius: 16px !important;
#     }
    
#     .stMarkdown {
#         color: #e0e0e0 !important;
#     }
    
#     hr {
#         border-color: rgba(255, 255, 255, 0.1) !important;
#         margin: 20px 0 !important;
#     }
    
#     h3 {
#         color: #b0b0b0 !important;
#         font-weight: 600 !important;
#         margin-top: 15px !important;
#     }
# </style>
# """, unsafe_allow_html=True)

# # -------------------------
# # Sidebar
# # -------------------------
# with st.sidebar:
#     st.markdown("### 📅 Meeting Scheduler")
#     st.markdown("---")

#     # Month navigation
#     col1, col2, col3 = st.columns([1, 2, 1])
#     col1.button("◀", key="prev_month", on_click=go_prev_month, use_container_width=True)
#     col2.markdown(f"<div style='text-align:center; padding-top:8px;'><strong>{cal_module.month_name[st.session_state.current_month]} {st.session_state.current_year}</strong></div>", unsafe_allow_html=True)
#     col3.button("▶", key="next_month", on_click=go_next_month, use_container_width=True)

#     # Calendar display
#     cal = cal_module.monthcalendar(st.session_state.current_year, st.session_state.current_month)
#     calendar_html = '<div class="calendar-grid">'
    
#     for day in ['Mo','Tu','We','Th','Fr','Sa','Su']:
#         calendar_html += f'<div class="calendar-day calendar-header">{day}</div>'
    
#     for week in cal:
#         for d in week:
#             if d == 0:
#                 calendar_html += '<div class="calendar-day"></div>'
#             else:
#                 is_today = (d == today.day and 
#                            st.session_state.current_month == today.month and 
#                            st.session_state.current_year == today.year)
#                 css = "calendar-today" if is_today else ""
#                 calendar_html += f'<div class="calendar-day {css}">{d}</div>'
    
#     calendar_html += '</div>'
#     st.markdown(calendar_html, unsafe_allow_html=True)
    
#     # Date selector
#     st.markdown("---")
#     st.markdown('<div class="blue-glass-section">', unsafe_allow_html=True)
#     st.markdown("**📅 View Events for Date:**")
    
#     date_input = st.text_input(
#         "Type date (DD/MM/YYYY)",
#         placeholder="28/11/2025",
#         key="manual_date_input",
#         help="Enter date in DD/MM/YYYY format"
#     )
    
#     if st.button("📅 View Events", use_container_width=True, key="view_events_btn"):
#         selected_date = None
        
#         if date_input.strip():
#             try:
#                 parts = date_input.strip().split('/')
#                 if len(parts) == 3:
#                     day, month, year = int(parts[0]), int(parts[1]), int(parts[2])
#                     selected_date = date(year, month, day)
#             except:
#                 st.error("❌ Invalid format! Use DD/MM/YYYY (e.g., 28/11/2025)")
        
#         if selected_date:
#             events = get_events_for_date(selected_date)
            
#             st.markdown(f"**📆 {selected_date.strftime('%A, %B %d, %Y')}**")
#             st.markdown("---")
            
#             if events:
#                 for event in events:
#                     st.markdown(f"### 🕐 {event['time']}")
#                     st.markdown(f"**{event['summary']}**")
#                     if event.get('description'):
#                         st.caption(event['description'])
#                     st.markdown("---")
#             else:
#                 st.info(f"✨ No events on {selected_date.strftime('%B %d')}")
#         else:
#             st.warning("⚠️ Please enter a date in DD/MM/YYYY format")
    
#     st.markdown('</div>', unsafe_allow_html=True)

#     st.markdown("---")
#     st.markdown('<div class="purple-glass-section">', unsafe_allow_html=True)
#     st.markdown("### 📋 Upcoming Events")
#     try:
#         events = get_upcoming_events(5)
#         if events:
#             for ev in events:
#                 start = ev['start'].get('dateTime', ev['start'].get('date'))
#                 formatted_time = format_event_time(start)
#                 st.markdown(f"**{ev.get('summary','Untitled')}**")
#                 st.caption(formatted_time)
#                 st.markdown("---")
#         else:
#             st.info("No upcoming events")
#     except Exception as e:
#         st.warning(f"Could not load events: {e}")
    
#     st.markdown('</div>', unsafe_allow_html=True)

#     st.markdown("---")
#     st.markdown("### 💡 How to use")
#     st.markdown("- Click 🎤 to speak or type\n- Say/type: 'Schedule meeting tomorrow at 3pm'\n- Click confirmation to book")
    
#     if st.button("🗑️ Clear chat", use_container_width=True):
#         for key in defaults.keys():
#             st.session_state[key] = defaults[key]
#         st.rerun()

# # -------------------------
# # Main content
# # -------------------------
# st.markdown('<div class="main-header">🤖 AI Meeting Scheduler Agent</div>', unsafe_allow_html=True)
# st.markdown('<div class="sub-header">Schedule meetings using natural language or voice 🎤</div>', unsafe_allow_html=True)

# # Render chat messages
# for msg in st.session_state.messages:
#     with st.chat_message(msg["role"]):
#         st.markdown(msg["content"], unsafe_allow_html=True)

# # Inject STT component
# stt_component()

# # FIXED: Chat input processing with duplicate prevention
# user_input = st.chat_input("Type your meeting request or click 🎤 to speak...")

# if user_input and not st.session_state.processing:
#     st.session_state.processing = True
    
#     # Add user message
#     st.session_state.messages.append({"role":"user","content":user_input})
#     with st.chat_message("user"):
#         st.markdown(user_input)

#     # Process request
#     with st.chat_message("assistant"):
#         with st.spinner("🔍 Analyzing your request..."):
#             parsed = parse_meeting_request(user_input)
            
#             if not parsed:
#                 err = "❌ Couldn't understand. Try: 'Schedule meeting tomorrow at 3pm for 30 minutes'"
#                 st.markdown(err)
#                 st.session_state.messages.append({"role":"assistant","content":err})
#             else:
#                 # VALIDATION: Check if requested time is in the past
#                 requested_datetime = parse_datetime_from_parsed_data(parsed)
#                 current_time = datetime.now(LOCAL_TZ)
                
#                 if requested_datetime and requested_datetime < current_time:
#                     time_diff = current_time - requested_datetime
                    
#                     if time_diff.total_seconds() < 300:  # Less than 5 minutes ago
#                         err = "⏰ **That time just passed!**\n\nPlease schedule for a future time. Try adding a few minutes or hours."
#                     elif time_diff.days > 0:
#                         err = f"📅 **That date has already passed!**\n\nYou requested: {requested_datetime.strftime('%A, %B %d at %I:%M %p')}\n\nPlease choose a future date."
#                     else:
#                         err = f"⏰ **That time has already passed today!**\n\nYou requested: {requested_datetime.strftime('%I:%M %p')}\nCurrent time: {current_time.strftime('%I:%M %p')}\n\nPlease choose a future time."
                    
#                     st.markdown(err)
#                     st.session_state.messages.append({"role":"assistant","content":err})
#                 else:
#                     suggestion = suggest_best_slot(parsed)
#                     st.session_state.pending_parsed_data = parsed
#                     st.session_state.current_suggestion = suggestion

#                     if not suggestion.get("success"):
#                         err = f"❌ {suggestion.get('message','Unable to find slots')}"
#                         st.markdown(err)
#                         st.session_state.messages.append({"role":"assistant","content":err})
#                     else:
#                         if suggestion.get("conflict"):
#                             conflict = suggestion["conflict"]
#                             response = f"""⚠️ **Event Conflict Detected!**

# 🚫 **Existing Event at Requested Time:**
# - **Event Name:** {conflict.get('summary','Untitled')}
# - **Time:** {conflict['start'].strftime('%a, %b %d at %I:%M %p')} - {conflict['end'].strftime('%I:%M %p')}

# ✅ **Available Alternative Slots:**
# - **Title:** {parsed.get('title')}
# - **Duration:** {parsed.get('duration_minutes')} minutes

# 👇 Click on any available time slot below.
# """
#                             st.markdown(response)
#                             st.session_state.messages.append({"role":"assistant","content":response})
#                             st.session_state.pending_slot = None
#                             st.session_state.selected_alternative = None
#                         else:
#                             slot = suggestion["slot"]
#                             st.session_state.pending_slot = slot
#                             formatted = format_slot_for_display(slot)
#                             response = f"""✅ **Found slot**

# 📅 **{parsed.get('title')}**
# - **When:** {formatted['full_display']}
# - **Duration:** {parsed.get('duration_minutes')} minutes

# Click 'Confirm & Create Event' to book.
# """
#                             st.markdown(response)
#                             st.session_state.messages.append({"role":"assistant","content":response})
    
#     st.session_state.processing = False
#     st.rerun()

# # Pending confirm message
# if st.session_state._pending_confirm_msg:
#     msg = st.session_state._pending_confirm_msg
#     last = st.session_state.messages[-1]["content"] if st.session_state.messages else None
#     if last != msg:
#         st.session_state.messages.append({"role":"assistant","content":msg})
#     st.session_state._pending_confirm_msg = None

# # Alternative slot buttons
# if st.session_state.current_suggestion and st.session_state.current_suggestion.get("alternatives"):
#     suggestion = st.session_state.current_suggestion
#     alts = suggestion.get("alternatives", [])
#     if alts:
#         st.markdown("---")
#         st.markdown("### 📅 Available Time Slots")
#         cols = st.columns(min(3, len(alts)))
#         for idx, slot in enumerate(alts):
#             formatted = format_slot_for_display(slot)
#             btn_key = f"alt_{idx}_{slot['start'].isoformat()}"
#             if cols[idx % 3].button(f"📅 {formatted['date']}\n⏰ {formatted['time_range']}", key=btn_key, use_container_width=True):
#                 st.session_state.pending_slot = slot
#                 st.session_state.selected_alternative = idx
#                 st.session_state._pending_confirm_msg = f"✅ Selected: **{formatted['full_display']}**\n\nClick 'Confirm & Create Event' below to book this slot."
#                 st.rerun()

# # Confirmation block
# if st.session_state.pending_slot:
#     st.markdown("---")
#     col1, col2, col3 = st.columns([1, 2, 1])
#     with col2:
#         if st.button("✅ Confirm & Create Event", type="primary", use_container_width=True, key="confirm_create"):
#             with st.spinner("📅 Creating event..."):
#                 try:
#                     slot = st.session_state.pending_slot
#                     parsed = st.session_state.pending_parsed_data
#                     created = create_event(
#                         summary=parsed.get("title","Meeting"),
#                         start_datetime=slot["start"],
#                         end_datetime=slot["end"],
#                         description=parsed.get("description","Created by AI Meeting Scheduler Agent"),
#                         attendees=parsed.get("attendees",[])
#                     )
#                     if created:
#                         formatted = format_slot_for_display(slot)
#                         event_link = created.get('htmlLink', '#')
#                         success = f"""🎉 **Event Created Successfully!**

# 📅 **{parsed.get('title','Meeting')}**
# - **Time:** {formatted['full_display']}

# [📱 View in Google Calendar]({event_link})
# """
#                         st.session_state.messages.append({"role":"assistant","content":success})
                        
#                         # Reset state
#                         st.session_state.pending_slot = None
#                         st.session_state.pending_parsed_data = None
#                         st.session_state.current_suggestion = None
#                         st.session_state.selected_alternative = None
                        
#                         st.success("✅ Event created successfully!")
#                         st.balloons()
#                         st.rerun()
#                     else:
#                         err = "❌ Failed to create event. Try again."
#                         st.session_state.messages.append({"role":"assistant","content":err})
#                         st.error(err)
#                 except Exception as e:
#                     err = f"❌ Error creating event: {e}"
#                     st.session_state.messages.append({"role":"assistant","content":err})
#                     st.error(err)

#         if st.button("❌ Cancel", use_container_width=True, key="cancel_create"):
#             st.session_state.pending_slot = None
#             st.session_state.pending_parsed_data = None
#             st.session_state.current_suggestion = None
#             st.session_state.selected_alternative = None
#             st.session_state._pending_confirm_msg = None
#             cancel_msg = "❌ Meeting request cancelled. Feel free to make a new request!"
#             last = st.session_state.messages[-1]["content"] if st.session_state.messages else None
#             if last != cancel_msg:
#                 st.session_state.messages.append({"role":"assistant","content":cancel_msg})
#             st.rerun()

# # Footer
# st.markdown("---")
# st.markdown('<div style="text-align:center;color:#999;font-size:0.9rem;">Powered by Google Calendar API | Built with Streamlit | 🎤 Voice enabled</div>', unsafe_allow_html=True)






















import streamlit as st
import calendar as cal_module
from datetime import datetime, timedelta
import pytz
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import your modules
from scheduler.gpt_parser import parse_meeting_request
from scheduler.scheduler_logic import suggest_best_slot, format_slot_for_display
from scheduler.google_calendar import get_calendar_service, create_event, get_upcoming_events, ensure_google_login
from groq import Groq

# Page config
st.set_page_config(page_title="AI Meeting Scheduler", page_icon="📅", layout="wide")

LOCAL_TZ = pytz.timezone('Asia/Kolkata')

# ---- GOOGLE LOGIN CHECK ----
with st.sidebar:
    st.title("🔐 Login")
    if not ensure_google_login():
        st.warning("Please log in to access your Google Calendar.")
        st.stop()
    else:
        st.success("✅ Logged in successfully!")

# ---- REST OF YOUR APP ----
st.title("📅 AI Meeting Scheduler")

# Your app logic continues here...

LOCAL_TZ = pytz.timezone('Asia/Kolkata')

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'input_text' not in st.session_state:
    st.session_state.input_text = ""
if 'audio_bytes' not in st.session_state:
    st.session_state.audio_bytes = None
if 'selected_month' not in st.session_state:
    st.session_state.selected_month = datetime.now(LOCAL_TZ)
if 'selected_date_for_view' not in st.session_state:
    st.session_state.selected_date_for_view = None
if 'pending_alternatives' not in st.session_state:
    st.session_state.pending_alternatives = None


# Custom CSS
st.markdown("""
<style>
    .stApp {
        background-color: #0e1117;
    }
    
    /* Hero Header */
    .hero-header {
        text-align: center;
        padding: 25px 20px;
        background: linear-gradient(135deg, #1e2130 0%, #262b3e 100%);
        border-radius: 16px;
        margin-bottom: 20px;
        border: 2px solid #2d3348;
    }
    
    .hero-title {
        font-size: 2rem;
        font-weight: 800;
        background: linear-gradient(135deg, #10b981 0%, #3b82f6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 5px;
    }
    
    .hero-subtitle {
        font-size: 1rem;
        color: #8b92a8;
    }
    
    /* Chat Container */
    .chat-container {
        background: linear-gradient(135deg, #1e2130 0%, #262b3e 100%);
        border-radius: 12px;
        padding: 20px;
        border: 1px solid #2d3348;
        min-height: 400px;
        max-height: 500px;
        overflow-y: auto;
        margin-bottom: 15px;
        display: flex;
        flex-direction: column;
    }
    
    /* Messages */
    .message-wrapper {
        display: flex;
        margin: 8px 0;
        width: 100%;
    }
    
    .message-wrapper.user {
        justify-content: flex-end;
    }
    
    .message-wrapper.agent {
        justify-content: flex-start;
    }
    
    .message {
        padding: 12px 16px;
        border-radius: 12px;
        max-width: 75%;
        word-wrap: break-word;
    }
    
    .user-message {
        background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
        color: white;
        border-radius: 18px 18px 4px 18px;
    }
    
    .agent-message {
        background: #1a1f2e;
        color: #ffffff;
        border: 1px solid #2d3348;
        border-radius: 18px 18px 18px 4px;
    }
    
    .message-label {
        font-size: 0.7rem;
        color: #8b92a8;
        margin-bottom: 6px;
        font-weight: 500;
    }
    
    .message-content {
        font-size: 0.95rem;
        line-height: 1.6;
    }
    
    /* Parsed data inline */
    .parsed-inline {
        display: inline-block;
        background: rgba(16, 185, 129, 0.1);
        padding: 4px 8px;
        border-radius: 6px;
        margin: 2px;
        color: #10b981;
        font-weight: 600;
    }
    
    /* Event Cards */
    .event-card {
        background: #1a1f2e;
        border-radius: 8px;
        padding: 10px;
        margin: 6px 0;
        border-left: 3px solid #3b82f6;
    }
    
    .event-title {
        font-size: 0.95rem;
        font-weight: 600;
        color: #ffffff;
        margin-bottom: 3px;
    }
    
    .event-time {
        font-size: 0.8rem;
        color: #8b92a8;
    }
    
    /* Success box */
    .success-box {
        background: rgba(16, 185, 129, 0.1);
        border: 2px solid #10b981;
        border-radius: 8px;
        padding: 15px;
        margin: 10px 0;
        text-align: center;
    }
    
    .success-title {
        font-size: 1.2rem;
        font-weight: 700;
        color: #10b981;
        margin-bottom: 8px;
    }
    
    .success-link {
        font-size: 0.9rem;
        color: #3b82f6;
        text-decoration: none;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("### 📅 Mini Calendar")
    
    # Month navigation
    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        if st.button("◀", key="prev_month"):
            st.session_state.selected_month -= timedelta(days=30)
            st.rerun()
    with col2:
        st.markdown(f"<div style='text-align: center; color: white; font-weight: 600;'>{st.session_state.selected_month.strftime('%B %Y')}</div>", unsafe_allow_html=True)
    with col3:
        if st.button("▶", key="next_month"):
            st.session_state.selected_month += timedelta(days=30)
            st.rerun()
    
    # Generate mini calendar
    year = st.session_state.selected_month.year
    month = st.session_state.selected_month.month
    month_cal = cal_module.monthcalendar(year, month)
    
    # Day headers
    days = ['Mo', 'Tu', 'We', 'Th', 'Fr', 'Sa', 'Su']
    cols = st.columns(7)
    for i, day in enumerate(days):
        cols[i].markdown(f"<div style='text-align: center; color: #8b92a8; font-size: 0.7rem; font-weight: 600;'>{day}</div>", unsafe_allow_html=True)
    
    # Calendar days
    today = datetime.now(LOCAL_TZ).date()
    for week in month_cal:
        cols = st.columns(7)
        for i, day in enumerate(week):
            if day == 0:
                cols[i].write("")
            else:
                date_obj = datetime(year, month, day).date()
                is_today = date_obj == today
                
                if cols[i].button(str(day), key=f"day_{day}", use_container_width=True):
                    st.session_state.selected_date_for_view = date_obj
                    st.rerun()
    
    st.markdown("---")
    
    # Display events for selected date
    st.markdown("### 📅 View Events for Date")
    if st.session_state.selected_date_for_view:
        st.markdown(f"**Events on {st.session_state.selected_date_for_view.strftime('%d %b %Y')}:**")
        
        try:
            service = get_calendar_service()
            day_start = LOCAL_TZ.localize(datetime.combine(st.session_state.selected_date_for_view, datetime.min.time()))
            day_end = LOCAL_TZ.localize(datetime.combine(st.session_state.selected_date_for_view, datetime.max.time()))
            
            events_result = service.events().list(
                calendarId='primary',
                timeMin=day_start.isoformat(),
                timeMax=day_end.isoformat(),
                singleEvents=True,
                orderBy='startTime'
            ).execute()
            
            events = events_result.get('items', [])
            
            if events:
                for event in events:
                    if 'dateTime' in event['start']:
                        start = datetime.fromisoformat(event['start']['dateTime'].replace('Z', '+00:00')).astimezone(LOCAL_TZ)
                        st.markdown(f"""
                        <div class="event-card">
                            <div class="event-title">{event.get('summary', 'Untitled')}</div>
                            <div class="event-time">🕐 {start.strftime('%I:%M %p')}</div>
                        </div>
                        """, unsafe_allow_html=True)
            else:
                st.info("No events on this day")
        except Exception as e:
            st.error(f"Error: {e}")
    
    st.markdown("---")
    
    # Upcoming Events
    st.markdown("### 📋 Upcoming Events")
    try:
        service = get_calendar_service()
        now = datetime.now(LOCAL_TZ)
        
        # Fetch upcoming events from now
        events_result = service.events().list(
            calendarId='primary',
            timeMin=now.isoformat(),
            maxResults=5,
            singleEvents=True,
            orderBy='startTime'
        ).execute()
        
        upcoming = events_result.get('items', [])
        
        if upcoming:
            for event in upcoming:
                start = event['start'].get('dateTime', event['start'].get('date'))
                if 'T' in start:  # It's a dateTime (not all-day event)
                    start_dt = datetime.fromisoformat(start.replace('Z', '+00:00')).astimezone(LOCAL_TZ)
                    st.markdown(f"""
                    <div class="event-card">
                        <div class="event-title">{event.get('summary', 'Untitled')}</div>
                        <div class="event-time">{start_dt.strftime('%a, %b %d at %I:%M %p')}</div>
                    </div>
                    """, unsafe_allow_html=True)
                else:  # All-day event
                    st.markdown(f"""
                    <div class="event-card">
                        <div class="event-title">{event.get('summary', 'Untitled')}</div>
                        <div class="event-time">📅 {start}</div>
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.info("No upcoming events")
    except Exception as e:
        st.error(f"Error: {e}")
        st.info("Make sure Google Calendar is connected")

# Main Content
st.markdown("""
<div class="hero-header">
    <div class="hero-title">⚡ AI Meeting Scheduler Agent</div>
    <div class="hero-subtitle">Schedule meetings using natural language or voice 🎤</div>
</div>
""", unsafe_allow_html=True)

# Chat Display Area
chat_container = st.container()

with chat_container:
    if len(st.session_state.messages) == 0:
        st.markdown("""
        <div class="message-wrapper agent">
            <div class="message agent-message">
                <div class="message-label">🤖 AI Assistant</div>
                <div class="message-content">
                    👋 Hi! I'm your AI scheduling assistant. Tell me what meeting you'd like to schedule.<br><br>
                    
             
        </div>
        """, unsafe_allow_html=True)
    
    for msg in st.session_state.messages:
        if msg['role'] == 'user':
            st.markdown(f"""
            <div class="message-wrapper user">
                <div class="message user-message">
                    <div class="message-label">You</div>
                    <div class="message-content">{msg['content']}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="message-wrapper agent">
                <div class="message agent-message">
                    <div class="message-label">⚡ AI Assistant</div>
                    <div class="message-content">{msg['content']}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    # Auto-scroll to bottom using JavaScript
    st.markdown("""
    <script>
        var chatContainer = window.parent.document.querySelector('.chat-container');
        if (chatContainer) {
            chatContainer.scrollTop = chatContainer.scrollHeight;
        }
    </script>
    """, unsafe_allow_html=True)

# Handle slot selection from alternatives
if st.session_state.pending_alternatives:
    st.markdown("**Choose an available time:**")
    cols = st.columns(3)
    
    for idx, alt in enumerate(st.session_state.pending_alternatives['slots'][:3]):
        formatted = format_slot_for_display(alt)
        with cols[idx]:
            if st.button(
                f"📅 {formatted['date']}\n🕐 {formatted['time_range']}", 
                key=f"slot_select_{idx}",
                use_container_width=True
            ):
                # Create event with selected slot
                with st.spinner("Creating event..."):
                    parsed = st.session_state.pending_alternatives['parsed']
                    event = create_event(
                        summary=parsed['title'],
                        start_datetime=alt['start'],
                        end_datetime=alt['end'],
                        description=parsed.get('description', ''),
                        attendees=parsed.get('attendees', [])
                    )
                    
                    if event:
                        # Add success message to chat
                        st.session_state.messages.append({
                            'role': 'agent',
                            'content': f"""
                            <div class="success-box">
                                <div class="success-title">🎉 Event Created Successfully!</div>
                                <div style="margin: 10px 0;">
                                    <strong>{parsed['title']}</strong><br>
                                    {formatted['full_display']}
                                </div>
                                <a href="{event.get('htmlLink', '#')}" target="_blank" class="success-link">
                                    📅 View Event in Google Calendar →
                                </a>
                            </div>
                            """
                        })
                        st.session_state.pending_alternatives = None
                        st.balloons()
                        st.rerun()
                    else:
                        st.error("Failed to create event")

# Input Area with Voice
st.markdown("---")

col1, col2, col3 = st.columns([8, 1, 1])

with col1:
    user_input = st.text_input(
        "Type your message...",
        value=st.session_state.input_text,
        key="chat_input",
        label_visibility="collapsed"
    )

with col2:
    send_clicked = st.button("➤", use_container_width=True, key="send_btn")

with col3:
    # Voice recording
    try:
        from audio_recorder_streamlit import audio_recorder
        
        audio_bytes = audio_recorder(
            text="",
            recording_color="#ef4444",
            neutral_color="#3b82f6",
            icon_name="microphone",
            icon_size="1x",
            key="audio_recorder"
        )
        
        if audio_bytes and audio_bytes != st.session_state.audio_bytes:
            st.session_state.audio_bytes = audio_bytes
            st.rerun()
            
    except ImportError:
        if st.button("🎤", use_container_width=True, key="mic_btn"):
            st.warning("Install audio-recorder-streamlit for voice input")

# Show audio player and transcribe button if audio exists
if st.session_state.audio_bytes:
    st.audio(st.session_state.audio_bytes, format="audio/wav")
    
    if st.button("📝 Transcribe Audio", use_container_width=True):
        with st.spinner("Transcribing..."):
            try:
                # Save audio temporarily
                with open("temp_audio.wav", "wb") as f:
                    f.write(st.session_state.audio_bytes)
                
                # Transcribe with Groq Whisper
                client = Groq(api_key=os.getenv('GROQ_API_KEY'))
                with open("temp_audio.wav", "rb") as audio_file:
                    transcription = client.audio.transcriptions.create(
                        file=audio_file,
                        model="whisper-large-v3"
                    )
                
                st.session_state.input_text = transcription.text
                st.session_state.audio_bytes = None  # Clear audio
                st.success(f"✅ Transcribed: {transcription.text}")
                st.rerun()
                
            except Exception as e:
                st.error(f"Transcription error: {e}")

# Process user message when send is clicked
if send_clicked and user_input.strip():
    # Add user message to chat
    st.session_state.messages.append({
        'role': 'user',
        'content': user_input
    })
    
    with st.spinner("🤖 Processing..."):
        # Parse with AI
        parsed = parse_meeting_request(user_input)
        
        if not parsed:
            st.session_state.messages.append({
                'role': 'agent',
                'content': "❌ I couldn't understand that. Please try rephrasing your request."
            })
            st.rerun()
        
        # Get suggestions
        suggestion = suggest_best_slot(parsed)
        
        # Build response based on suggestion
        if not suggestion['success']:
            # Past time error
            st.session_state.messages.append({
                'role': 'agent',
                'content': f"❌ {suggestion['message']}"
            })
        
        elif 'conflict' in suggestion:
            # Conflict detected
            conflict = suggestion['conflict']
            
            response_content = f"""
            📋 I found your meeting details:<br>
            <span class="parsed-inline">📌 {parsed['title']}</span>
            <span class="parsed-inline">📅 {parsed['date']}</span>
            <span class="parsed-inline">🕐 {parsed['time']}</span>
            <span class="parsed-inline">⏱️ {parsed['duration_minutes']} min</span>
            <br><br>
            ⚠️ <strong>Conflict detected:</strong> Your requested time overlaps with <strong>{conflict['summary']}</strong> 
            ({conflict['start'].strftime('%I:%M %p')} - {conflict['end'].strftime('%I:%M %p')})
            <br><br>
            I found {len(suggestion.get('alternatives', []))} alternative times. Please select one below:
            """
            
            st.session_state.messages.append({
                'role': 'agent',
                'content': response_content
            })
            
            # Store alternatives for selection
            st.session_state.pending_alternatives = {
                'slots': suggestion['alternatives'],
                'parsed': parsed
            }
        
        else:
            # No conflict - time available
            slot = suggestion['slot']
            formatted = format_slot_for_display(slot)
            
            # Create event immediately
            with st.spinner("Creating event..."):
                event = create_event(
                    summary=parsed['title'],
                    start_datetime=slot['start'],
                    end_datetime=slot['end'],
                    description=parsed.get('description', ''),
                    attendees=parsed.get('attendees', [])
                )
                
                if event:
                    response_content = f"""
                    ✅ Perfect! Your requested time is available.<br><br>
                    <div class="success-box">
                        <div class="success-title">🎉 Event Created Successfully!</div>
                        <div style="margin: 10px 0;">
                            <strong>{parsed['title']}</strong><br>
                            {formatted['full_display']}
                        </div>
                        <a href="{event.get('htmlLink', '#')}" target="_blank" class="success-link">
                            📅 View Event in Google Calendar →
                        </a>
                    </div>
                    """
                    st.session_state.messages.append({
                        'role': 'agent',
                        'content': response_content
                    })
                    st.balloons()
                else:
                    st.session_state.messages.append({
                        'role': 'agent',
                        'content': "❌ Failed to create the event. Please try again."
                    })
    
    # Clear input
    st.session_state.input_text = ""
    st.rerun()

# Footer
st.caption("💡 Powered by Groq AI & Google Calendar API")