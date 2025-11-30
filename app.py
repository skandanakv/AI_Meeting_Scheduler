# # import streamlit as st
# # import calendar as cal_module
# # from datetime import datetime, timedelta
# # import pytz
# # import sys
# # import os
# # import json

# # # Page config MUST BE FIRST - before any st.xxx commands!
# # st.set_page_config(page_title="AI Meeting Scheduler", page_icon="📅", layout="wide")

# # # Add parent directory to path (so scheduler package is importable)
# # sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# # # Import your modules
# # from scheduler.gpt_parser import parse_meeting_request
# # from scheduler.scheduler_logic import suggest_best_slot, format_slot_for_display
# # from scheduler.google_calendar import get_calendar_service, create_event, get_upcoming_events
# # from groq import Groq

# # # Local timezone
# # LOCAL_TZ = pytz.timezone('Asia/Kolkata')

# # # NOW you can use other st commands
# # # ---- CALENDAR CONNECTION CHECK ----
# # with st.sidebar:
# #     st.title("📅 Calendar Status")
# #     service = get_calendar_service()
# #     if service:
# #         st.success("✅ Connected to Skandana's Calendar")
# #     else:
# #         st.error("❌ Calendar connection failed. Check your secrets.")
# #         st.stop()

# # # ... rest of your code

# # # Test connection on startup






# # # ---- INITIALIZE SESSION STATE ----
# # if 'messages' not in st.session_state:
# #     st.session_state.messages = []
# # if 'input_text' not in st.session_state:
# #     st.session_state.input_text = ""
# # if 'audio_bytes' not in st.session_state:
# #     st.session_state.audio_bytes = None
# # if 'selected_month' not in st.session_state:
# #     st.session_state.selected_month = datetime.now(LOCAL_TZ)
# # if 'selected_date_for_view' not in st.session_state:
# #     st.session_state.selected_date_for_view = None
# # if 'pending_alternatives' not in st.session_state:
# #     st.session_state.pending_alternatives = None

# # # ---- APP TITLE ----
# # st.title("📅 AI Meeting Scheduler")

# # # Custom CSS
# # st.markdown("""
# # <style>
# #     .stApp {
# #         background-color: #0e1117;
# #     }
    
# #     /* Hero Header */
# #     .hero-header {
# #         text-align: center;
# #         padding: 25px 20px;
# #         background: linear-gradient(135deg, #1e2130 0%, #262b3e 100%);
# #         border-radius: 16px;
# #         margin-bottom: 20px;
# #         border: 2px solid #2d3348;
# #     }
    
# #     .hero-title {
# #         font-size: 2rem;
# #         font-weight: 800;
# #         background: linear-gradient(135deg, #10b981 0%, #3b82f6 100%);
# #         -webkit-background-clip: text;
# #         -webkit-text-fill-color: transparent;
# #         margin-bottom: 5px;
# #     }
    
# #     .hero-subtitle {
# #         font-size: 1rem;
# #         color: #8b92a8;
# #     }
    
# #     /* Chat Container */
# #     .chat-container {
# #         background: linear-gradient(135deg, #1e2130 0%, #262b3e 100%);
# #         border-radius: 12px;
# #         padding: 20px;
# #         border: 1px solid #2d3348;
# #         min-height: 400px;
# #         max-height: 500px;
# #         overflow-y: auto;
# #         margin-bottom: 15px;
# #         display: flex;
# #         flex-direction: column;
# #     }
    
# #     /* Messages */
# #     .message-wrapper {
# #         display: flex;
# #         margin: 8px 0;
# #         width: 100%;
# #     }
    
# #     .message-wrapper.user {
# #         justify-content: flex-end;
# #     }
    
# #     .message-wrapper.agent {
# #         justify-content: flex-start;
# #     }
    
# #     .message {
# #         padding: 12px 16px;
# #         border-radius: 12px;
# #         max-width: 75%;
# #         word-wrap: break-word;
# #     }
    
# #     .user-message {
# #         background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
# #         color: white;
# #         border-radius: 18px 18px 4px 18px;
# #     }
    
# #     .agent-message {
# #         background: #1a1f2e;
# #         color: #ffffff;
# #         border: 1px solid #2d3348;
# #         border-radius: 18px 18px 18px 4px;
# #     }
    
# #     .message-label {
# #         font-size: 0.7rem;
# #         color: #8b92a8;
# #         margin-bottom: 6px;
# #         font-weight: 500;
# #     }
    
# #     .message-content {
# #         font-size: 0.95rem;
# #         line-height: 1.6;
# #     }
    
# #     /* Parsed data inline */
# #     .parsed-inline {
# #         display: inline-block;
# #         background: rgba(16, 185, 129, 0.1);
# #         padding: 4px 8px;
# #         border-radius: 6px;
# #         margin: 2px;
# #         color: #10b981;
# #         font-weight: 600;
# #     }
    
# #     /* Event Cards */
# #     .event-card {
# #         background: #1a1f2e;
# #         border-radius: 8px;
# #         padding: 10px;
# #         margin: 6px 0;
# #         border-left: 3px solid #3b82f6;
# #     }
    
# #     .event-title {
# #         font-size: 0.95rem;
# #         font-weight: 600;
# #         color: #ffffff;
# #         margin-bottom: 3px;
# #     }
    
# #     .event-time {
# #         font-size: 0.8rem;
# #         color: #8b92a8;
# #     }
    
# #     /* Success box */
# #     .success-box {
# #         background: rgba(16, 185, 129, 0.1);
# #         border: 2px solid #10b981;
# #         border-radius: 8px;
# #         padding: 15px;
# #         margin: 10px 0;
# #         text-align: center;
# #     }
    
# #     .success-title {
# #         font-size: 1.2rem;
# #         font-weight: 700;
# #         color: #10b981;
# #         margin-bottom: 8px;
# #     }
    
# #     .success-link {
# #         font-size: 0.9rem;
# #         color: #3b82f6;
# #         text-decoration: none;
# #     }
# # </style>
# # """, unsafe_allow_html=True)

# # # Sidebar
# # with st.sidebar:
# #     st.markdown("### 📅 Mini Calendar")
    
# #     # Month navigation
# #     col1, col2, col3 = st.columns([1, 2, 1])
# #     with col1:
# #         if st.button("◀", key="prev_month"):
# #             st.session_state.selected_month -= timedelta(days=30)
# #             st.rerun()
# #     with col2:
# #         st.markdown(f"<div style='text-align: center; color: white; font-weight: 600;'>{st.session_state.selected_month.strftime('%B %Y')}</div>", unsafe_allow_html=True)
# #     with col3:
# #         if st.button("▶", key="next_month"):
# #             st.session_state.selected_month += timedelta(days=30)
# #             st.rerun()
    
# #     # Generate mini calendar
# #     year = st.session_state.selected_month.year
# #     month = st.session_state.selected_month.month
# #     month_cal = cal_module.monthcalendar(year, month)
    
# #     # Day headers
# #     days = ['Mo', 'Tu', 'We', 'Th', 'Fr', 'Sa', 'Su']
# #     cols = st.columns(7)
# #     for i, day in enumerate(days):
# #         cols[i].markdown(f"<div style='text-align: center; color: #8b92a8; font-size: 0.7rem; font-weight: 600;'>{day}</div>", unsafe_allow_html=True)
    
# #     # Calendar days
# #     today = datetime.now(LOCAL_TZ).date()
# #     for week in month_cal:
# #         cols = st.columns(7)
# #         for i, day in enumerate(week):
# #             if day == 0:
# #                 cols[i].write("")
# #             else:
# #                 date_obj = datetime(year, month, day).date()
# #                 is_today = date_obj == today
                
# #                 if cols[i].button(str(day), key=f"day_{day}", use_container_width=True):
# #                     st.session_state.selected_date_for_view = date_obj
# #                     st.rerun()
    
# #     st.markdown("---")
    
# #     # Display events for selected date
# #     st.markdown("### 📅 View Events for Date")
# #     if st.session_state.selected_date_for_view:
# #         st.markdown(f"**Events on {st.session_state.selected_date_for_view.strftime('%d %b %Y')}:**")
        
# #         try:
# #             service = get_calendar_service()
# #             day_start = LOCAL_TZ.localize(datetime.combine(st.session_state.selected_date_for_view, datetime.min.time()))
# #             day_end = LOCAL_TZ.localize(datetime.combine(st.session_state.selected_date_for_view, datetime.max.time()))
            
# #             events_result = service.events().list(
# #                 calendarId='primary',
# #                 timeMin=day_start.isoformat(),
# #                 timeMax=day_end.isoformat(),
# #                 singleEvents=True,
# #                 orderBy='startTime'
# #             ).execute()
            
# #             events = events_result.get('items', [])
            
# #             if events:
# #                 for event in events:
# #                     if 'dateTime' in event['start']:
# #                         start = datetime.fromisoformat(event['start']['dateTime'].replace('Z', '+00:00')).astimezone(LOCAL_TZ)
# #                         st.markdown(f"""
# #                         <div class="event-card">
# #                             <div class="event-title">{event.get('summary', 'Untitled')}</div>
# #                             <div class="event-time">🕐 {start.strftime('%I:%M %p')}</div>
# #                         </div>
# #                         """, unsafe_allow_html=True)
# #             else:
# #                 st.info("No events on this day")
# #         except Exception as e:
# #             st.error(f"Error: {e}")
    
# #     st.markdown("---")
    
# #     # Upcoming Events
# #     st.markdown("### 📋 Upcoming Events")
# #     try:
# #         service = get_calendar_service()
# #         now = datetime.now(LOCAL_TZ)
        
# #         # Fetch upcoming events from now
# #         events_result = service.events().list(
# #             calendarId='primary',
# #             timeMin=now.isoformat(),
# #             maxResults=5,
# #             singleEvents=True,
# #             orderBy='startTime'
# #         ).execute()
        
# #         upcoming = events_result.get('items', [])
        
# #         if upcoming:
# #             for event in upcoming:
# #                 start = event['start'].get('dateTime', event['start'].get('date'))
# #                 if 'T' in start:  # It's a dateTime (not all-day event)
# #                     start_dt = datetime.fromisoformat(start.replace('Z', '+00:00')).astimezone(LOCAL_TZ)
# #                     st.markdown(f"""
# #                     <div class="event-card">
# #                         <div class="event-title">{event.get('summary', 'Untitled')}</div>
# #                         <div class="event-time">{start_dt.strftime('%a, %b %d at %I:%M %p')}</div>
# #                     </div>
# #                     """, unsafe_allow_html=True)
# #                 else:  # All-day event
# #                     st.markdown(f"""
# #                     <div class="event-card">
# #                         <div class="event-title">{event.get('summary', 'Untitled')}</div>
# #                         <div class="event-time">📅 {start}</div>
# #                     </div>
# #                     """, unsafe_allow_html=True)
# #         else:
# #             st.info("No upcoming events")
# #     except Exception as e:
# #         st.error(f"Error: {e}")
# #         st.info("Make sure Google Calendar is connected")

# # # Main Content
# # st.markdown("""
# # <div class="hero-header">
# #     <div class="hero-title">⚡ AI Meeting Scheduler Agent</div>
# #     <div class="hero-subtitle">Schedule meetings using natural language or voice 🎤</div>
# # </div>
# # """, unsafe_allow_html=True)

# # # Chat Display Area
# # chat_container = st.container()

# # with chat_container:
# #     if len(st.session_state.messages) == 0:
# #         st.markdown("""
# #         <div class="message-wrapper agent">
# #             <div class="message agent-message">
# #                 <div class="message-label">🤖 AI Assistant</div>
# #                 <div class="message-content">
# #                     👋 Hi! I'm your AI scheduling assistant. Tell me what meeting you'd like to schedule.<br><br>
                    
             
# #         </div>
# #         """, unsafe_allow_html=True)
    
# #     for msg in st.session_state.messages:
# #         if msg['role'] == 'user':
# #             st.markdown(f"""
# #             <div class="message-wrapper user">
# #                 <div class="message user-message">
# #                     <div class="message-label">You</div>
# #                     <div class="message-content">{msg['content']}</div>
# #                 </div>
# #             </div>
# #             """, unsafe_allow_html=True)
# #         else:
# #             st.markdown(f"""
# #             <div class="message-wrapper agent">
# #                 <div class="message agent-message">
# #                     <div class="message-label">⚡ AI Assistant</div>
# #                     <div class="message-content">{msg['content']}</div>
# #                 </div>
# #             </div>
# #             """, unsafe_allow_html=True)
    
# #     # Auto-scroll to bottom using JavaScript
# #     st.markdown("""
# #     <script>
# #         var chatContainer = window.parent.document.querySelector('.chat-container');
# #         if (chatContainer) {
# #             chatContainer.scrollTop = chatContainer.scrollHeight;
# #         }
# #     </script>
# #     """, unsafe_allow_html=True)

# # # Handle slot selection from alternatives
# # if st.session_state.pending_alternatives:
# #     st.markdown("**Choose an available time:**")
# #     cols = st.columns(3)
    
# #     for idx, alt in enumerate(st.session_state.pending_alternatives['slots'][:3]):
# #         formatted = format_slot_for_display(alt)
# #         with cols[idx]:
# #             if st.button(
# #                 f"📅 {formatted['date']}\n🕐 {formatted['time_range']}", 
# #                 key=f"slot_select_{idx}",
# #                 use_container_width=True
# #             ):
# #                 # Create event with selected slot
# #                 with st.spinner("Creating event..."):
# #                     parsed = st.session_state.pending_alternatives['parsed']
# #                     event = create_event(
# #                         summary=parsed['title'],
# #                         start_datetime=alt['start'],
# #                         end_datetime=alt['end'],
# #                         description=parsed.get('description', ''),
# #                         attendees=parsed.get('attendees', [])
# #                     )
                    
# #                     if event:
# #                         # Add success message to chat
# #                         st.session_state.messages.append({
# #                             'role': 'agent',
# #                             'content': f"""
# #                             <div class="success-box">
# #                                 <div class="success-title">🎉 Event Created Successfully!</div>
# #                                 <div style="margin: 10px 0;">
# #                                     <strong>{parsed['title']}</strong><br>
# #                                     {formatted['full_display']}
# #                                 </div>
# #                                 <a href="{event.get('htmlLink', '#')}" target="_blank" class="success-link">
# #                                     📅 View Event in Google Calendar →
# #                                 </a>
# #                             </div>
# #                             """
# #                         })
# #                         st.session_state.pending_alternatives = None
# #                         st.balloons()
# #                         st.rerun()
# #                     else:
# #                         st.error("Failed to create event")

# # # Input Area with Voice
# # st.markdown("---")

# # col1, col2, col3 = st.columns([8, 1, 1])

# # with col1:
# #     user_input = st.text_input(
# #         "Type your message...",
# #         value=st.session_state.input_text,
# #         key="chat_input",
# #         label_visibility="collapsed"
# #     )

# # with col2:
# #     send_clicked = st.button("➤", use_container_width=True, key="send_btn")

# # with col3:
# #     # Voice recording
# #     try:
# #         from audio_recorder_streamlit import audio_recorder
        
# #         audio_bytes = audio_recorder(
# #             text="",
# #             recording_color="#ef4444",
# #             neutral_color="#3b82f6",
# #             icon_name="microphone",
# #             icon_size="1x",
# #             key="audio_recorder"
# #         )
        
# #         if audio_bytes and audio_bytes != st.session_state.audio_bytes:
# #             st.session_state.audio_bytes = audio_bytes
# #             st.rerun()
            
# #     except ImportError:
# #         if st.button("🎤", use_container_width=True, key="mic_btn"):
# #             st.warning("Install audio-recorder-streamlit for voice input")

# # # Show audio player and transcribe button if audio exists
# # if st.session_state.audio_bytes:
# #     st.audio(st.session_state.audio_bytes, format="audio/wav")
    
# #     if st.button("📝 Transcribe Audio", use_container_width=True):
# #         with st.spinner("Transcribing..."):
# #             try:
# #                 # Save audio temporarily
# #                 with open("temp_audio.wav", "wb") as f:
# #                     f.write(st.session_state.audio_bytes)
                
# #                 # Transcribe with Groq Whisper
# #                 client = Groq(api_key=os.getenv('GROQ_API_KEY'))
# #                 with open("temp_audio.wav", "rb") as audio_file:
# #                     transcription = client.audio.transcriptions.create(
# #                         file=audio_file,
# #                         model="whisper-large-v3"
# #                     )
                
# #                 st.session_state.input_text = transcription.text
# #                 st.session_state.audio_bytes = None  # Clear audio
# #                 st.success(f"✅ Transcribed: {transcription.text}")
# #                 st.rerun()
                
# #             except Exception as e:
# #                 st.error(f"Transcription error: {e}")

# # # Process user message when send is clicked
# # # Process user message when send is clicked
# # if send_clicked and user_input.strip():
# #     # Add user message to chat
# #     st.session_state.messages.append({
# #         'role': 'user',
# #         'content': user_input
# #     })
    
# #     # Clear input immediately to prevent reprocessing
# #     st.session_state.input_text = ""
    
# #     with st.spinner("🤖 Processing..."):
# #         # Parse with AI
# #         parsed = parse_meeting_request(user_input)
        
# #         if not parsed:
# #             st.session_state.messages.append({
# #                 'role': 'agent',
# #                 'content': "❌ I couldn't understand that. Please try rephrasing your request."
# #             })
# #             st.rerun()
        
# #         # Get suggestions
# #         suggestion = suggest_best_slot(parsed)
        
# #         # Build response based on suggestion
# #         if not suggestion['success']:
# #             # Past time error
# #             st.session_state.messages.append({
# #                 'role': 'agent',
# #                 'content': f"❌ {suggestion['message']}"
# #             })
        
# #         elif 'conflict' in suggestion:
# #             # Conflict detected
# #             conflict = suggestion['conflict']
            
# #             response_content = f"""
# #             📋 I found your meeting details:<br>
# #             <span class="parsed-inline">📌 {parsed['title']}</span>
# #             <span class="parsed-inline">📅 {parsed['date']}</span>
# #             <span class="parsed-inline">🕐 {parsed['time']}</span>
# #             <span class="parsed-inline">⏱️ {parsed['duration_minutes']} min</span>
# #             <br><br>
# #             ⚠️ <strong>Conflict detected:</strong> Your requested time overlaps with <strong>{conflict['summary']}</strong> 
# #             ({conflict['start'].strftime('%I:%M %p')} - {conflict['end'].strftime('%I:%M %p')})
# #             <br><br>
# #             I found {len(suggestion.get('alternatives', []))} alternative times. Please select one below:
# #             """
            
# #             st.session_state.messages.append({
# #                 'role': 'agent',
# #                 'content': response_content
# #             })
            
# #             # Store alternatives for selection
# #             st.session_state.pending_alternatives = {
# #                 'slots': suggestion['alternatives'],
# #                 'parsed': parsed
# #             }
        
# #         else:
# #             # No conflict - time available
# #             slot = suggestion['slot']
# #             formatted = format_slot_for_display(slot)
            
# #             # Create event immediately
# #             with st.spinner("Creating event..."):
# #                 event = create_event(
# #                     summary=parsed['title'],
# #                     start_datetime=slot['start'],
# #                     end_datetime=slot['end'],
# #                     description=parsed.get('description', ''),
# #                     attendees=parsed.get('attendees', [])
# #                 )
                
# #                 if event:
# #                     response_content = f"""
# #                     ✅ Perfect! Your requested time is available.<br><br>
# #                     <div class="success-box">
# #                         <div class="success-title">🎉 Event Created Successfully!</div>
# #                         <div style="margin: 10px 0;">
# #                             <strong>{parsed['title']}</strong><br>
# #                             {formatted['full_display']}
# #                         </div>
# #                         <a href="{event.get('htmlLink', '#')}" target="_blank" class="success-link">
# #                             📅 View Event in Google Calendar →
# #                         </a>
# #                     </div>
# #                     """
# #                     st.session_state.messages.append({
# #                         'role': 'agent',
# #                         'content': response_content
# #                     })
# #                     st.balloons()
# #                 else:
# #                     st.session_state.messages.append({
# #                         'role': 'agent',
# #                         'content': "❌ Failed to create the event. Please try again."
# #                     })
    
# #     # Clear input
# #     st.session_state.input_text = ""
# #     st.rerun()

# # # Footer
# # st.caption("💡 Powered by Groq AI & Google Calendar API")






































# import streamlit as st
# import calendar as cal_module
# from datetime import datetime, timedelta
# import pytz
# import sys
# import os
# import json

# # Page config MUST BE FIRST - before any st.xxx commands!
# st.set_page_config(page_title="AI Meeting Scheduler", page_icon="📅", layout="wide")

# # Add parent directory to path (so scheduler package is importable)
# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# # Import your modules
# from scheduler.gpt_parser import parse_meeting_request
# from scheduler.scheduler_logic import suggest_best_slot, format_slot_for_display
# from scheduler.google_calendar import get_calendar_service, create_event, get_upcoming_events
# from groq import Groq

# # Local timezone
# LOCAL_TZ = pytz.timezone('Asia/Kolkata')

# # NOW you can use other st commands
# # ---- CALENDAR CONNECTION CHECK ----
# with st.sidebar:
#     st.title("📅 Calendar Status")
#     service = get_calendar_service()
#     if service:
#         st.success("✅ Connected to Skandana's Calendar")
#     else:
#         st.error("❌ Calendar connection failed. Check your secrets.")
#         st.stop()

# # ... rest of your code

# # Test connection on startup






# # ---- INITIALIZE SESSION STATE ----
# if 'messages' not in st.session_state:
#     st.session_state.messages = []
# if 'input_text' not in st.session_state:
#     st.session_state.input_text = ""
# if 'audio_bytes' not in st.session_state:
#     st.session_state.audio_bytes = None
# if 'selected_month' not in st.session_state:
#     st.session_state.selected_month = datetime.now(LOCAL_TZ)
# if 'selected_date_for_view' not in st.session_state:
#     st.session_state.selected_date_for_view = None
# if 'pending_alternatives' not in st.session_state:
#     st.session_state.pending_alternatives = None

# # ---- APP TITLE ----
# st.title("📅 AI Meeting Scheduler")

# # Custom CSS
# st.markdown("""
# <style>
#     .stApp {
#         background-color: #0e1117;
#     }
    
#     /* Hero Header */
#     .hero-header {
#         text-align: center;
#         padding: 25px 20px;
#         background: linear-gradient(135deg, #1e2130 0%, #262b3e 100%);
#         border-radius: 16px;
#         margin-bottom: 20px;
#         border: 2px solid #2d3348;
#     }
    
#     .hero-title {
#         font-size: 2rem;
#         font-weight: 800;
#         background: linear-gradient(135deg, #10b981 0%, #3b82f6 100%);
#         -webkit-background-clip: text;
#         -webkit-text-fill-color: transparent;
#         margin-bottom: 5px;
#     }
    
#     .hero-subtitle {
#         font-size: 1rem;
#         color: #8b92a8;
#     }
    
#     /* Chat Container */
#     .chat-container {
#         background: linear-gradient(135deg, #1e2130 0%, #262b3e 100%);
#         border-radius: 12px;
#         padding: 20px;
#         border: 1px solid #2d3348;
#         min-height: 400px;
#         max-height: 500px;
#         overflow-y: auto;
#         margin-bottom: 15px;
#         display: flex;
#         flex-direction: column;
#     }
    
#     /* Messages */
#     .message-wrapper {
#         display: flex;
#         margin: 8px 0;
#         width: 100%;
#     }
    
#     .message-wrapper.user {
#         justify-content: flex-end;
#     }
    
#     .message-wrapper.agent {
#         justify-content: flex-start;
#     }
    
#     .message {
#         padding: 12px 16px;
#         border-radius: 12px;
#         max-width: 75%;
#         word-wrap: break-word;
#     }
    
#     .user-message {
#         background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
#         color: white;
#         border-radius: 18px 18px 4px 18px;
#     }
    
#     .agent-message {
#         background: #1a1f2e;
#         color: #ffffff;
#         border: 1px solid #2d3348;
#         border-radius: 18px 18px 18px 4px;
#     }
    
#     .message-label {
#         font-size: 0.7rem;
#         color: #8b92a8;
#         margin-bottom: 6px;
#         font-weight: 500;
#     }
    
#     .message-content {
#         font-size: 0.95rem;
#         line-height: 1.6;
#     }
    
#     /* Parsed data inline */
#     .parsed-inline {
#         display: inline-block;
#         background: rgba(16, 185, 129, 0.1);
#         padding: 4px 8px;
#         border-radius: 6px;
#         margin: 2px;
#         color: #10b981;
#         font-weight: 600;
#     }
    
#     /* Event Cards */
#     .event-card {
#         background: #1a1f2e;
#         border-radius: 8px;
#         padding: 10px;
#         margin: 6px 0;
#         border-left: 3px solid #3b82f6;
#     }
    
#     .event-title {
#         font-size: 0.95rem;
#         font-weight: 600;
#         color: #ffffff;
#         margin-bottom: 3px;
#     }
    
#     .event-time {
#         font-size: 0.8rem;
#         color: #8b92a8;
#     }
    
#     /* Success box */
#     .success-box {
#         background: rgba(16, 185, 129, 0.1);
#         border: 2px solid #10b981;
#         border-radius: 8px;
#         padding: 15px;
#         margin: 10px 0;
#         text-align: center;
#     }
    
#     .success-title {
#         font-size: 1.2rem;
#         font-weight: 700;
#         color: #10b981;
#         margin-bottom: 8px;
#     }
    
#     .success-link {
#         font-size: 0.9rem;
#         color: #3b82f6;
#         text-decoration: none;
#     }
# </style>
# """, unsafe_allow_html=True)

# # Sidebar
# with st.sidebar:
#     st.markdown("### 📅 Mini Calendar")
    
#     # Month navigation
#     col1, col2, col3 = st.columns([1, 2, 1])
#     with col1:
#         if st.button("◀", key="prev_month"):
#             st.session_state.selected_month -= timedelta(days=30)
#             st.rerun()
#     with col2:
#         st.markdown(f"<div style='text-align: center; color: white; font-weight: 600;'>{st.session_state.selected_month.strftime('%B %Y')}</div>", unsafe_allow_html=True)
#     with col3:
#         if st.button("▶", key="next_month"):
#             st.session_state.selected_month += timedelta(days=30)
#             st.rerun()
    
#     # Generate mini calendar
#     year = st.session_state.selected_month.year
#     month = st.session_state.selected_month.month
#     month_cal = cal_module.monthcalendar(year, month)
    
#     # Day headers
#     days = ['Mo', 'Tu', 'We', 'Th', 'Fr', 'Sa', 'Su']
#     cols = st.columns(7)
#     for i, day in enumerate(days):
#         cols[i].markdown(f"<div style='text-align: center; color: #8b92a8; font-size: 0.7rem; font-weight: 600;'>{day}</div>", unsafe_allow_html=True)
    
#     # Calendar days
#     today = datetime.now(LOCAL_TZ).date()
#     for week in month_cal:
#         cols = st.columns(7)
#         for i, day in enumerate(week):
#             if day == 0:
#                 cols[i].write("")
#             else:
#                 date_obj = datetime(year, month, day).date()
#                 is_today = date_obj == today
                
#                 if cols[i].button(str(day), key=f"day_{day}", use_container_width=True):
#                     st.session_state.selected_date_for_view = date_obj
#                     st.rerun()
    
#     st.markdown("---")
    
#     # Display events for selected date
#     st.markdown("### 📅 View Events for Date")
#     if st.session_state.selected_date_for_view:
#         st.markdown(f"**Events on {st.session_state.selected_date_for_view.strftime('%d %b %Y')}:**")
        
#         try:
#             service = get_calendar_service()
#             day_start = LOCAL_TZ.localize(datetime.combine(st.session_state.selected_date_for_view, datetime.min.time()))
#             day_end = LOCAL_TZ.localize(datetime.combine(st.session_state.selected_date_for_view, datetime.max.time()))
            
#             events_result = service.events().list(
#                 calendarId='primary',
#                 timeMin=day_start.isoformat(),
#                 timeMax=day_end.isoformat(),
#                 singleEvents=True,
#                 orderBy='startTime'
#             ).execute()
            
#             events = events_result.get('items', [])
            
#             if events:
#                 for event in events:
#                     if 'dateTime' in event['start']:
#                         start = datetime.fromisoformat(event['start']['dateTime'].replace('Z', '+00:00')).astimezone(LOCAL_TZ)
#                         st.markdown(f"""
#                         <div class="event-card">
#                             <div class="event-title">{event.get('summary', 'Untitled')}</div>
#                             <div class="event-time">🕐 {start.strftime('%I:%M %p')}</div>
#                         </div>
#                         """, unsafe_allow_html=True)
#             else:
#                 st.info("No events on this day")
#         except Exception as e:
#             st.error(f"Error: {e}")
    
#     st.markdown("---")
    
#     # Upcoming Events
#     st.markdown("### 📋 Upcoming Events")
#     try:
#         service = get_calendar_service()
#         now = datetime.now(LOCAL_TZ)
        
#         # Fetch upcoming events from now
#         events_result = service.events().list(
#             calendarId='primary',
#             timeMin=now.isoformat(),
#             maxResults=5,
#             singleEvents=True,
#             orderBy='startTime'
#         ).execute()
        
#         upcoming = events_result.get('items', [])
        
#         if upcoming:
#             for event in upcoming:
#                 start = event['start'].get('dateTime', event['start'].get('date'))
#                 if 'T' in start:  # It's a dateTime (not all-day event)
#                     start_dt = datetime.fromisoformat(start.replace('Z', '+00:00')).astimezone(LOCAL_TZ)
#                     st.markdown(f"""
#                     <div class="event-card">
#                         <div class="event-title">{event.get('summary', 'Untitled')}</div>
#                         <div class="event-time">{start_dt.strftime('%a, %b %d at %I:%M %p')}</div>
#                     </div>
#                     """, unsafe_allow_html=True)
#                 else:  # All-day event
#                     st.markdown(f"""
#                     <div class="event-card">
#                         <div class="event-title">{event.get('summary', 'Untitled')}</div>
#                         <div class="event-time">📅 {start}</div>
#                     </div>
#                     """, unsafe_allow_html=True)
#         else:
#             st.info("No upcoming events")
#     except Exception as e:
#         st.error(f"Error: {e}")
#         st.info("Make sure Google Calendar is connected")

# # Main Content
# st.markdown("""
# <div class="hero-header">
#     <div class="hero-title">⚡ AI Meeting Scheduler Agent</div>
#     <div class="hero-subtitle">Schedule meetings using natural language or voice 🎤</div>
# </div>
# """, unsafe_allow_html=True)

# # Chat Display Area
# chat_container = st.container()

# with chat_container:
#     if len(st.session_state.messages) == 0:
#         st.markdown("""
#         <div class="message-wrapper agent">
#             <div class="message agent-message">
#                 <div class="message-label">🤖 AI Assistant</div>
#                 <div class="message-content">
#                     👋 Hi! I'm your AI scheduling assistant. Tell me what meeting you'd like to schedule.<br><br>
                    
             
#         </div>
#         """, unsafe_allow_html=True)
    
#     for msg in st.session_state.messages:
#         if msg['role'] == 'user':
#             st.markdown(f"""
#             <div class="message-wrapper user">
#                 <div class="message user-message">
#                     <div class="message-label">You</div>
#                     <div class="message-content">{msg['content']}</div>
#                 </div>
#             </div>
#             """, unsafe_allow_html=True)
#         else:
#             st.markdown(f"""
#             <div class="message-wrapper agent">
#                 <div class="message agent-message">
#                     <div class="message-label">⚡ AI Assistant</div>
#                     <div class="message-content">{msg['content']}</div>
#                 </div>
#             </div>
#             """, unsafe_allow_html=True)
    
#     # Auto-scroll to bottom using JavaScript
#     st.markdown("""
#     <script>
#         var chatContainer = window.parent.document.querySelector('.chat-container');
#         if (chatContainer) {
#             chatContainer.scrollTop = chatContainer.scrollHeight;
#         }
#     </script>
#     """, unsafe_allow_html=True)

# # Handle slot selection from alternatives
# if st.session_state.pending_alternatives:
#     st.markdown("**Choose an available time:**")
#     cols = st.columns(3)
    
#     for idx, alt in enumerate(st.session_state.pending_alternatives['slots'][:3]):
#         formatted = format_slot_for_display(alt)
#         with cols[idx]:
#             if st.button(
#                 f"📅 {formatted['date']}\n🕐 {formatted['time_range']}", 
#                 key=f"slot_select_{idx}",
#                 use_container_width=True
#             ):
#                 # Create event with selected slot
#                 with st.spinner("Creating event..."):
#                     parsed = st.session_state.pending_alternatives['parsed']
                    
#                     # FIXED: Extract title properly
#                     event_title = parsed.get('title') or parsed.get('summary') or 'Untitled Meeting'
                    
#                     event = create_event(
#                         summary=event_title,
#                         start_datetime=alt['start'],
#                         end_datetime=alt['end'],
#                         description=parsed.get('description', ''),
#                         attendees=parsed.get('attendees', [])
#                     )
                    
#                     if event:
#                         # Add success message to chat
#                         st.session_state.messages.append({
#                             'role': 'agent',
#                             'content': f"""
#                             <div class="success-box">
#                                 <div class="success-title">🎉 Event Created Successfully!</div>
#                                 <div style="margin: 10px 0;">
#                                     <strong>{event_title}</strong><br>
#                                     {formatted['full_display']}
#                                 </div>
#                                 <a href="{event.get('htmlLink', '#')}" target="_blank" class="success-link">
#                                     📅 View Event in Google Calendar →
#                                 </a>
#                             </div>
#                             """
#                         })
#                         st.session_state.pending_alternatives = None
#                         st.balloons()
#                         st.rerun()
#                     else:
#                         st.error("Failed to create event")

# # Input Area with Voice
# st.markdown("---")

# col1, col2, col3 = st.columns([8, 1, 1])

# with col1:
#     user_input = st.text_input(
#         "Type your message...",
#         value="",,
#         key="chat_input",
#         label_visibility="collapsed"
#         placeholder="Type your message..."  # Add placeholder instead
#     )

# with col2:
#     send_clicked = st.button("➤", use_container_width=True, key="send_btn")

# with col3:
#     # Voice recording
#     try:
#         from audio_recorder_streamlit import audio_recorder
        
#         audio_bytes = audio_recorder(
#             text="",
#             recording_color="#ef4444",
#             neutral_color="#3b82f6",
#             icon_name="microphone",
#             icon_size="1x",
#             key="audio_recorder"
#         )
        
#         if audio_bytes and audio_bytes != st.session_state.audio_bytes:
#             st.session_state.audio_bytes = audio_bytes
#             st.rerun()
            
#     except ImportError:
#         if st.button("🎤", use_container_width=True, key="mic_btn"):
#             st.warning("Install audio-recorder-streamlit for voice input")

# # Show audio player and transcribe button if audio exists
# if st.session_state.audio_bytes:
#     st.audio(st.session_state.audio_bytes, format="audio/wav")
    
#     if st.button("📝 Transcribe Audio", use_container_width=True):
#         with st.spinner("Transcribing..."):
#             try:
#                 # Save audio temporarily
#                 with open("temp_audio.wav", "wb") as f:
#                     f.write(st.session_state.audio_bytes)
                
#                 # Transcribe with Groq Whisper
#                 client = Groq(api_key=os.getenv('GROQ_API_KEY'))
#                 with open("temp_audio.wav", "rb") as audio_file:
#                     transcription = client.audio.transcriptions.create(
#                         file=audio_file,
#                         model="whisper-large-v3"
#                     )
                
#                 st.session_state.input_text = transcription.text
#                 st.session_state.audio_bytes = None  # Clear audio
#                 st.success(f"✅ Transcribed: {transcription.text}")
#                 st.rerun()
                
#             except Exception as e:
#                 st.error(f"Transcription error: {e}")

# # Process user message when send is clicked
# if send_clicked and user_input.strip():
#     # Add user message to chat
#     st.session_state.messages.append({
#         'role': 'user',
#         'content': user_input
#     })
    
#     # Clear input immediately to prevent reprocessing
#     st.session_state.input_text = ""
    
#     with st.spinner("🤖 Processing..."):
#         # Parse with AI
#         parsed = parse_meeting_request(user_input)
        
#         # DEBUG: Print parsed data
#         print(f"🔍 DEBUG - Parsed data: {json.dumps(parsed, indent=2, default=str)}")
        
#         if not parsed:
#             st.session_state.messages.append({
#                 'role': 'agent',
#                 'content': "❌ I couldn't understand that. Please try rephrasing your request."
#             })
#             st.session_state.pending_alternatives = None  # ✅ ADD THIS LINE
#             st.rerun()
        
#         # FIXED: Extract title properly
#         event_title = parsed.get('title') or parsed.get('summary') or 'Untitled Meeting'
        
#         # Get suggestions
#         suggestion = suggest_best_slot(parsed)
        
#         # Build response based on suggestion
#         if not suggestion['success']:
#             # Past time error
#             st.session_state.messages.append({
#                 'role': 'agent',
#                 'content': f"❌ {suggestion['message']}"
#             })
#             st.session_state.pending_alternatives = None  # ✅ ADD THIS LINE
        
#         elif 'conflict' in suggestion:
#             # Conflict detected
#             conflict = suggestion['conflict']
            
#             response_content = f"""
#             📋 I found your meeting details:<br>
#             <span class="parsed-inline">📌 {event_title}</span>
#             <span class="parsed-inline">📅 {parsed['date']}</span>
#             <span class="parsed-inline">🕐 {parsed['time']}</span>
#             <span class="parsed-inline">⏱️ {parsed['duration_minutes']} min</span>
#             <br><br>
#             ⚠️ <strong>Conflict detected:</strong> Your requested time overlaps with <strong>{conflict['summary']}</strong> 
#             ({conflict['start'].strftime('%I:%M %p')} - {conflict['end'].strftime('%I:%M %p')})
#             <br><br>
#             I found {len(suggestion.get('alternatives', []))} alternative times. Please select one below:
#             """
            
#             st.session_state.messages.append({
#                 'role': 'agent',
#                 'content': response_content
#             })
            
#             # Store alternatives for selection
#             st.session_state.pending_alternatives = {
#                 'slots': suggestion['alternatives'],
#                 'parsed': parsed
#             }
        
#         else:
#             # No conflict - time available
#             slot = suggestion['slot']
#             formatted = format_slot_for_display(slot)
            
#             # Create event immediately
#             with st.spinner("Creating event..."):
#                 event = create_event(
#                     summary=event_title,
#                     start_datetime=slot['start'],
#                     end_datetime=slot['end'],
#                     description=parsed.get('description', ''),
#                     attendees=parsed.get('attendees', [])
#                 )
                
#                 if event:
#                     response_content = f"""
#                     ✅ Perfect! Your requested time is available.<br><br>
#                     <div class="success-box">
#                         <div class="success-title">🎉 Event Created Successfully!</div>
#                         <div style="margin: 10px 0;">
#                             <strong>{event_title}</strong><br>
#                             {formatted['full_display']}
#                         </div>
#                         <a href="{event.get('htmlLink', '#')}" target="_blank" class="success-link">
#                             📅 View Event in Google Calendar →
#                         </a>
#                     </div>
#                     """
#                     st.session_state.messages.append({
#                         'role': 'agent',
#                         'content': response_content
#                     })
#                     st.session_state.pending_alternatives = None 
#                     st.balloons()
#                 else:
#                     st.session_state.messages.append({
#                         'role': 'agent',
#                         'content': "❌ Failed to create the event. Please try again."
#                     })
#                     st.session_state.pending_alternatives = None
    
#     # Clear input
#     st.session_state.input_text = ""
#     st.rerun()

# # Footer
# st.caption("💡 Powered by Groq AI & Google Calendar API")

















import streamlit as st
import calendar as cal_module
from datetime import datetime, timedelta
import pytz
import sys
import os
import json

# Page config MUST BE FIRST - before any st.xxx commands!
st.set_page_config(page_title="AI Meeting Scheduler", page_icon="📅", layout="wide")

# Add parent directory to path (so scheduler package is importable)
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import your modules
from scheduler.gpt_parser import parse_meeting_request
from scheduler.scheduler_logic import suggest_best_slot, format_slot_for_display
from scheduler.google_calendar import get_calendar_service, create_event, get_upcoming_events
from groq import Groq

# Local timezone
LOCAL_TZ = pytz.timezone('Asia/Kolkata')

# NOW you can use other st commands
# ---- CALENDAR CONNECTION CHECK ----
with st.sidebar:
    st.title("📅 Calendar Status")
    service = get_calendar_service()
    if service:
        st.success("✅ Connected to Skandana's Calendar")
    else:
        st.error("❌ Calendar connection failed. Check your secrets.")
        st.stop()

# ... rest of your code

# Test connection on startup






# ---- INITIALIZE SESSION STATE ----
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
if 'input_key' not in st.session_state:
    st.session_state.input_key = 0

# ---- APP TITLE ----
st.title("📅 AI Meeting Scheduler")

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
                    
                    # FIXED: Extract title properly
                    event_title = parsed.get('title') or parsed.get('summary') or 'Untitled Meeting'
                    
                    event = create_event(
                        summary=event_title,
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
                                    <strong>{event_title}</strong><br>
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
        value="",
        key=f"chat_input_{st.session_state.input_key}",
        label_visibility="collapsed",
        placeholder="Type your message..."
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
                
                transcribed_text = transcription.text
                
                # Clear audio immediately
                st.session_state.audio_bytes = None
                
                # Add user message to chat
                st.session_state.messages.append({
                    'role': 'user',
                    'content': transcribed_text
                })
                
                # Increment key to clear text input
                st.session_state.input_key += 1
                
                # Process the transcribed message (same logic as text input)
                with st.spinner("🤖 Processing..."):
                    parsed = parse_meeting_request(transcribed_text)
                    
                    if not parsed:
                        st.session_state.messages.append({
                            'role': 'agent',
                            'content': "❌ I couldn't understand that. Please try rephrasing your request."
                        })
                        st.session_state.pending_alternatives = None
                        st.rerun()
                    
                    event_title = parsed.get('title') or parsed.get('summary') or 'Untitled Meeting'
                    suggestion = suggest_best_slot(parsed)
                    
                    if not suggestion['success']:
                        st.session_state.messages.append({
                            'role': 'agent',
                            'content': f"❌ {suggestion['message']}"
                        })
                        st.session_state.pending_alternatives = None
                    
                    elif 'conflict' in suggestion:
                        conflict = suggestion['conflict']
                        response_content = f"""
                        📋 I found your meeting details:<br>
                        <span class="parsed-inline">📌 {event_title}</span>
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
                        st.session_state.pending_alternatives = {
                            'slots': suggestion['alternatives'],
                            'parsed': parsed
                        }
                    
                    else:
                        slot = suggestion['slot']
                        formatted = format_slot_for_display(slot)
                        
                        with st.spinner("Creating event..."):
                            event = create_event(
                                summary=event_title,
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
                                        <strong>{event_title}</strong><br>
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
                                st.session_state.pending_alternatives = None
                                st.balloons()
                            else:
                                st.session_state.messages.append({
                                    'role': 'agent',
                                    'content': "❌ Failed to create the event. Please try again."
                                })
                                st.session_state.pending_alternatives = None
                
                st.rerun()
                
            except Exception as e:
                st.error(f"Transcription error: {e}")
                st.session_state.audio_bytes = None

# Process user message when send is clicked
if send_clicked and user_input.strip():
    # Add user message to chat
    st.session_state.messages.append({
        'role': 'user',
        'content': user_input
    })
    
    # Increment key to clear text input
    st.session_state.input_key += 1
    
    with st.spinner("🤖 Processing..."):
        # Parse with AI
        parsed = parse_meeting_request(user_input)
        
        # DEBUG: Print parsed data
        print(f"🔍 DEBUG - Parsed data: {json.dumps(parsed, indent=2, default=str)}")
        
        if not parsed:
            st.session_state.messages.append({
                'role': 'agent',
                'content': "❌ I couldn't understand that. Please try rephrasing your request."
            })
            st.session_state.pending_alternatives = None
            st.rerun()
        
        # FIXED: Extract title properly
        event_title = parsed.get('title') or parsed.get('summary') or 'Untitled Meeting'
        
        # Get suggestions
        suggestion = suggest_best_slot(parsed)
        
        # Build response based on suggestion
        if not suggestion['success']:
            # Past time error
            st.session_state.messages.append({
                'role': 'agent',
                'content': f"❌ {suggestion['message']}"
            })
            st.session_state.pending_alternatives = None
        
        elif 'conflict' in suggestion:
            # Conflict detected
            conflict = suggestion['conflict']
            
            response_content = f"""
            📋 I found your meeting details:<br>
            <span class="parsed-inline">📌 {event_title}</span>
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
                    summary=event_title,
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
                            <strong>{event_title}</strong><br>
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
                    st.session_state.pending_alternatives = None
                    st.balloons()
                else:
                    st.session_state.messages.append({
                        'role': 'agent',
                        'content': "❌ Failed to create the event. Please try again."
                    })
                    st.session_state.pending_alternatives = None
    
    st.rerun()

# Footer
st.caption("💡 Powered by Groq AI & Google Calendar API")













