# import streamlit as st
# import pandas as pd
# import plotly.graph_objects as go
# from datetime import datetime, timedelta
# import pytz
# import calendar as cal_module
# import sys
# import os

# # Add parent directory to path
# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# from scheduler.google_calendar import get_calendar_service

# st.set_page_config(page_title="Calendar Heatmap", page_icon="", layout="wide")

# LOCAL_TZ = pytz.timezone('Asia/Kolkata')

# # Custom CSS for dark, clean UI
# st.markdown("""
# <style>
#     /* Dark theme */
#     .stApp {
#         background-color: #0e1117;
#     }
    
#     /* Header styling */
#     .heatmap-header {
#         text-align: center;
#         padding: 20px 0;
#         margin-bottom: 30px;
#     }
    
#     .heatmap-title {
#         font-size: 2.5rem;
#         font-weight: 700;
#         color: #ffffff;
#         margin-bottom: 8px;
#     }
    
#     .heatmap-subtitle {
#         font-size: 1.1rem;
#         color: #8b92a8;
#     }
    
#     /* Metric cards */
#     .metric-card {
#         background: linear-gradient(135deg, #1e2130 0%, #262b3e 100%);
#         border-radius: 12px;
#         padding: 20px;
#         border: 1px solid #2d3348;
#         transition: transform 0.2s;
#     }
    
#     .metric-card:hover {
#         transform: translateY(-2px);
#         border-color: #4a5568;
#     }
    
#     .metric-label {
#         font-size: 0.9rem;
#         color: #8b92a8;
#         margin-bottom: 8px;
#         font-weight: 500;
#     }
    
#     .metric-value {
#         font-size: 2rem;
#         font-weight: 700;
#         color: #ffffff;
#     }
    
#     .metric-delta {
#         font-size: 0.85rem;
#         margin-top: 4px;
#     }
    
#     .metric-delta.positive {
#         color: #10b981;
#     }
    
#     .metric-delta.negative {
#         color: #ef4444;
#     }
    
#     .metric-delta.neutral {
#         color: #8b92a8;
#     }
    
#     /* Calendar grid */
#     .calendar-container {
#         background: linear-gradient(135deg, #1e2130 0%, #262b3e 100%);
#         border-radius: 16px;
#         padding: 30px;
#         border: 1px solid #2d3348;
#         margin: 20px 0;
#     }
    
#     /* Insight cards */
#     .insight-card {
#         background: linear-gradient(135deg, #1e2130 0%, #262b3e 100%);
#         border-radius: 12px;
#         padding: 18px;
#         border-left: 4px solid;
#         margin: 10px 0;
#     }
    
#     .insight-warning {
#         border-left-color: #f59e0b;
#     }
    
#     .insight-success {
#         border-left-color: #10b981;
#     }
    
#     .insight-info {
#         border-left-color: #3b82f6;
#     }
    
#     /* Day details */
#     .day-detail {
#         background: #1a1f2e;
#         border-radius: 8px;
#         padding: 12px 16px;
#         margin: 8px 0;
#         border-left: 3px solid #3b82f6;
#     }
    
#     .meeting-time {
#         color: #8b92a8;
#         font-size: 0.9rem;
#     }
    
#     .meeting-title {
#         color: #ffffff;
#         font-size: 1rem;
#         font-weight: 500;
#         margin-top: 4px;
#     }
    
#     /* Time slot bars */
#     .time-bar {
#         background: #1a1f2e;
#         border-radius: 6px;
#         padding: 8px 12px;
#         margin: 6px 0;
#         display: flex;
#         align-items: center;
#         justify-content: space-between;
#     }
    
#     .time-label {
#         color: #8b92a8;
#         font-size: 0.9rem;
#         min-width: 80px;
#     }
    
#     .time-bar-fill {
#         height: 20px;
#         border-radius: 4px;
#         background: linear-gradient(90deg, #10b981, #059669);
#         transition: width 0.3s;
#     }
    
#     .time-count {
#         color: #ffffff;
#         font-weight: 600;
#         margin-left: 10px;
#     }
# </style>
# """, unsafe_allow_html=True)

# # Header
# st.markdown("""
# <div class="heatmap-header">
#     <div class="heatmap-title">🔥 Calendar Heatmap</div>
#     <div class="heatmap-subtitle">Visual overview of your meeting patterns</div>
# </div>
# """, unsafe_allow_html=True)

# # Month selector
# # Month selector
# col1, col2, col3 = st.columns([2, 3, 2])
# with col2:
#     today = datetime.now(LOCAL_TZ)
    
#     # Generate list of months: 6 months back + current + 6 months forward
#     months = []
    
#     # Add past 6 months
#     for i in range(6, 0, -1):
#         date = today - timedelta(days=30*i)
#         months.append(date.strftime("%B %Y"))
    
#     # Add current month
#     months.append(today.strftime("%B %Y"))
    
#     # Add next 6 months
#     for i in range(1, 7):
#         date = today + timedelta(days=30*i)
#         months.append(date.strftime("%B %Y"))
    
#     selected_month_str = st.selectbox(
#         "📅 Select Month",
#         months,
#         index=6,  # Default to current month (middle of list)
#         key="month_selector"
#     )
    
#     # Parse selected month
#     selected_date = datetime.strptime(selected_month_str, "%B %Y")
#     selected_date = LOCAL_TZ.localize(selected_date)
    
#     # Parse selected month
#     selected_date = datetime.strptime(selected_month_str, "%B %Y")
#     selected_date = LOCAL_TZ.localize(selected_date)

# st.markdown("---")

# # Function to fetch meetings for a month
# def fetch_month_data(year, month):
#     service = get_calendar_service()
#     first_day = LOCAL_TZ.localize(datetime(year, month, 1, 0, 0, 0))
#     last_day_num = cal_module.monthrange(year, month)[1]
#     last_day = LOCAL_TZ.localize(datetime(year, month, last_day_num, 23, 59, 59))
    
#     events_result = service.events().list(
#         calendarId='primary',
#         timeMin=first_day.isoformat(),
#         timeMax=last_day.isoformat(),
#         singleEvents=True,
#         orderBy='startTime'
#     ).execute()
    
#     events = events_result.get('items', [])
    
#     daily_meetings = {}
#     meeting_details = {}
#     hourly_counts = {}
    
#     for event in events:
#         if 'dateTime' in event['start']:
#             start = datetime.fromisoformat(event['start']['dateTime'].replace('Z', '+00:00'))
#             start_local = start.astimezone(LOCAL_TZ)
#             date_key = start_local.date()
#             hour_key = start_local.hour
            
#             # Count meetings per day
#             daily_meetings[date_key] = daily_meetings.get(date_key, 0) + 1
            
#             # Count meetings per hour
#             hourly_counts[hour_key] = hourly_counts.get(hour_key, 0) + 1
            
#             # Store meeting details
#             if date_key not in meeting_details:
#                 meeting_details[date_key] = []
            
#             meeting_details[date_key].append({
#                 'title': event.get('summary', 'Untitled'),
#                 'start': start_local,
#                 'end': datetime.fromisoformat(event['end']['dateTime'].replace('Z', '+00:00')).astimezone(LOCAL_TZ)
#             })
    
#     return daily_meetings, meeting_details, hourly_counts

# # Fetch current month data
# try:
#     with st.spinner(f"📊 Loading meetings for {selected_month_str}..."):
#         daily_meetings, meeting_details, hourly_counts = fetch_month_data(
#             selected_date.year, 
#             selected_date.month
#         )
        
#         # Fetch previous month data for comparison
#         prev_month_date = selected_date - timedelta(days=30)
#         prev_daily_meetings, _, _ = fetch_month_data(
#             prev_month_date.year,
#             prev_month_date.month
#         )
        
#         # Create calendar heatmap
#         month_cal = cal_module.monthcalendar(selected_date.year, selected_date.month)
        
#         # Prepare data for heatmap
#         z_data = []
#         hover_text = []
#         customdata = []
        
#         # Define proper color thresholds
#         def get_color_for_count(count):
#             if count == 0:
#                 return 0
#             elif count <= 2:
#                 return 0.25
#             elif count <= 4:
#                 return 0.5
#             elif count <= 6:
#                 return 0.75
#             else:
#                 return 1.0
        
#         for week in month_cal:
#             week_counts = []
#             week_hover = []
#             week_dates = []
#             for day_num in week:
#                 if day_num == 0:
#                     week_counts.append(None)
#                     week_hover.append("")
#                     week_dates.append(None)
#                 else:
#                     date_obj = datetime(selected_date.year, selected_date.month, day_num).date()
#                     count = daily_meetings.get(date_obj, 0)
#                     week_counts.append(count)
#                     week_hover.append(f"{date_obj.strftime('%B %d, %Y')}<br>{count} meeting{'s' if count != 1 else ''}")
#                     week_dates.append(date_obj)
            
#             z_data.append(week_counts)
#             hover_text.append(week_hover)
#             customdata.append(week_dates)
        
#         # Create heatmap with FIXED color scale
#         fig = go.Figure(data=go.Heatmap(
#             z=z_data,
#             x=['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
#             y=[f"Week {i+1}" for i in range(len(month_cal))],
#             colorscale=[
#                 [0, '#161b22'],      # 0 meetings - dark
#                 [0.25, '#0e4429'],   # 1-2 meetings - light green
#                 [0.5, '#006d32'],    # 3-4 meetings - medium green  
#                 [0.75, '#26a641'],   # 5-6 meetings - bright green
#                 [1.0, '#39d353']     # 7+ meetings - very bright green
#             ],
#             hovertemplate='%{hovertext}<extra></extra>',
#             hovertext=hover_text,
#             showscale=True,
#             colorbar=dict(
#                 title="Meetings",
#                 titleside="right",
#                 tickmode="linear",
#                 tick0=0,
#                 dtick=2
#             ),
#             zmin=0,
#             zmax=max([x for row in z_data for x in row if x is not None], default=7)
#         ))
        
#         fig.update_layout(
#             title=dict(
#                 text=f"📅 {selected_month_str}",
#                 font=dict(size=20, color='white'),
#                 x=0.5,
#                 xanchor='center'
#             ),
#             xaxis=dict(
#                 side='top',
#                 showgrid=False,
#                 zeroline=False,
#                 color='white'
#             ),
#             yaxis=dict(
#                 showgrid=False,
#                 zeroline=False,
#                 color='white',
#                 autorange='reversed'
#             ),
#             plot_bgcolor='#1e2130',
#             paper_bgcolor='#1e2130',
#             height=400,
#             margin=dict(l=60, r=60, t=80, b=40),
#             font=dict(color='white')
#         )
        
#         st.plotly_chart(fig, use_container_width=True)
        
#         # Calculate metrics
#         total_meetings = sum(daily_meetings.values())
#         last_day_num = cal_module.monthrange(selected_date.year, selected_date.month)[1]
#         free_days = last_day_num - len(daily_meetings)
#         avg_per_day = total_meetings / last_day_num if last_day_num > 0 else 0
        
#         # Previous month metrics
#         prev_total = sum(prev_daily_meetings.values())
#         prev_days = cal_module.monthrange(prev_month_date.year, prev_month_date.month)[1]
#         prev_avg = prev_total / prev_days if prev_days > 0 else 0
        
#         # Calculate changes
#         meetings_change = total_meetings - prev_total
#         meetings_pct = (meetings_change / prev_total * 100) if prev_total > 0 else 0
#         avg_change = avg_per_day - prev_avg
        
#         # Find busiest day
#         if daily_meetings:
#             busiest_date = max(daily_meetings, key=daily_meetings.get)
#             busiest_count = daily_meetings[busiest_date]
#             busiest_day_str = busiest_date.strftime('%A, %B %d, %Y')
#         else:
#             busiest_day_str = "No meetings"
#             busiest_count = 0
        
#         st.markdown("---")
        
#         # Metrics row with comparison
#         col1, col2, col3, col4 = st.columns(4)
        
#         with col1:
#             delta_class = "positive" if meetings_change < 0 else "negative" if meetings_change > 0 else "neutral"
#             delta_symbol = "↓" if meetings_change < 0 else "↑" if meetings_change > 0 else "→"
#             st.markdown(f"""
#             <div class="metric-card">
#                 <div class="metric-label">📊 Total Meetings</div>
#                 <div class="metric-value">{total_meetings}</div>
#                 <div class="metric-delta {delta_class}">{delta_symbol} {abs(meetings_change)} vs last month</div>
#             </div>
#             """, unsafe_allow_html=True)
        
#         with col2:
#             st.markdown(f"""
#             <div class="metric-card">
#                 <div class="metric-label">🔥 Busiest Day</div>
#                 <div class="metric-value">{busiest_count}</div>
#                 <div class="metric-delta neutral">{busiest_date.strftime('%b %d') if daily_meetings else 'N/A'}</div>
#             </div>
#             """, unsafe_allow_html=True)
        
#         with col3:
#             st.markdown(f"""
#             <div class="metric-card">
#                 <div class="metric-label">✨ Free Days</div>
#                 <div class="metric-value">{free_days}</div>
#                 <div class="metric-delta neutral">{(free_days/last_day_num*100):.0f}% of month</div>
#             </div>
#             """, unsafe_allow_html=True)
        
#         with col4:
#             avg_delta_class = "positive" if avg_change < 0 else "negative" if avg_change > 0 else "neutral"
#             avg_symbol = "↓" if avg_change < 0 else "↑" if avg_change > 0 else "→"
#             st.markdown(f"""
#             <div class="metric-card">
#                 <div class="metric-label">📈 Daily Average</div>
#                 <div class="metric-value">{avg_per_day:.1f}</div>
#                 <div class="metric-delta {avg_delta_class}">{avg_symbol} {abs(avg_change):.1f} vs last month</div>
#             </div>
#             """, unsafe_allow_html=True)
        
#         st.markdown("---")
        
#         # NEW: Time of Day Analysis
#         st.markdown("### ⏰ Peak Meeting Hours")
        
#         if hourly_counts:
#             # Create time slots (9am to 6pm)
#             time_slots = range(9, 18)
#             max_hour_count = max(hourly_counts.values()) if hourly_counts else 1
            
#             col1, col2 = st.columns([2, 1])
            
#             with col1:
#                 for hour in time_slots:
#                     count = hourly_counts.get(hour, 0)
#                     bar_width = (count / max_hour_count * 100) if max_hour_count > 0 else 0
#                     time_label = f"{hour % 12 if hour % 12 != 0 else 12}{'am' if hour < 12 else 'pm'}"
                    
#                     st.markdown(f"""
#                     <div class="time-bar">
#                         <span class="time-label">{time_label}</span>
#                         <div style="flex: 1; margin: 0 15px;">
#                             <div class="time-bar-fill" style="width: {bar_width}%;"></div>
#                         </div>
#                         <span class="time-count">{count}</span>
#                     </div>
#                     """, unsafe_allow_html=True)
            
#             with col2:
#                 if hourly_counts:
#                     peak_hour = max(hourly_counts, key=hourly_counts.get)
#                     peak_count = hourly_counts[peak_hour]
#                     peak_label = f"{peak_hour % 12 if peak_hour % 12 != 0 else 12}{'am' if peak_hour < 12 else 'pm'}"
                    
#                     st.markdown(f"""
#                     <div class="insight-card insight-info">
#                         <strong>🔥 Peak Hour</strong><br>
#                         <span style="font-size: 1.5rem; color: #10b981;">{peak_label}</span><br>
#                         <span style="color: #8b92a8;">{peak_count} meetings</span>
#                     </div>
#                     """, unsafe_allow_html=True)
#         else:
#             st.info("No meeting time data available for this month")
        
#         st.markdown("---")
        
#         # Insights section
#         st.markdown("### 🧠 Insights")
        
#         if daily_meetings:
#             st.markdown(f"""
#             <div class="insight-card insight-info">
#                 <strong>🔥 Busiest Day:</strong> {busiest_day_str} with {busiest_count} meeting{'s' if busiest_count != 1 else ''}
#             </div>
#             """, unsafe_allow_html=True)
            
#             # Comparison insight
#             if meetings_pct != 0:
#                 trend = "increased" if meetings_pct > 0 else "decreased"
#                 trend_class = "warning" if meetings_pct > 0 else "success"
#                 st.markdown(f"""
#                 <div class="insight-card insight-{trend_class}">
#                     <strong>📊 Monthly Trend:</strong> Your meetings {trend} by {abs(meetings_pct):.0f}% compared to {prev_month_date.strftime('%B')}
#                 </div>
#                 """, unsafe_allow_html=True)
            
#             if avg_per_day > 3:
#                 st.markdown(f"""
#                 <div class="insight-card insight-warning">
#                     <strong>⚠️ High Meeting Load:</strong> You're averaging {avg_per_day:.1f} meetings per day. Consider blocking focus time.
#                 </div>
#                 """, unsafe_allow_html=True)
#             elif avg_per_day < 1:
#                 st.markdown(f"""
#                 <div class="insight-card insight-success">
#                     <strong>✅ Healthy Balance:</strong> You have good focus time with only {avg_per_day:.1f} meetings per day on average.
#                 </div>
#                 """, unsafe_allow_html=True)
#         else:
#             st.info(f"✨ No meetings scheduled in {selected_month_str}")
        
#         st.markdown("---")
        
#         # NEW: Interactive Day Selector
#         st.markdown("### 📅 View Meetings by Day")
        
#         if daily_meetings:
#             # Create list of days with meetings
#             days_with_meetings = sorted(daily_meetings.keys(), reverse=True)
#             day_options = [d.strftime('%A, %B %d') for d in days_with_meetings]
            
#             selected_day_str = st.selectbox(
#                 "Select a day to view meetings:",
#                 ["Select a day..."] + day_options,
#                 key="day_selector"
#             )
            
#             if selected_day_str != "Select a day...":
#                 # Find the corresponding date
#                 selected_day = None
#                 for day in days_with_meetings:
#                     if day.strftime('%A, %B %d') == selected_day_str:
#                         selected_day = day
#                         break
                
#                 if selected_day and selected_day in meeting_details:
#                     meeting_count = daily_meetings[selected_day]
#                     st.markdown(f"#### 📋 {meeting_count} Meeting{'s' if meeting_count != 1 else ''} on {selected_day_str}")
                    
#                     for meeting in meeting_details[selected_day]:
#                         time_str = f"{meeting['start'].strftime('%I:%M %p')} - {meeting['end'].strftime('%I:%M %p')}"
#                         duration = (meeting['end'] - meeting['start']).total_seconds() / 60
#                         st.markdown(f"""
#                         <div class="day-detail">
#                             <div class="meeting-time">🕐 {time_str} ({duration:.0f} minutes)</div>
#                             <div class="meeting-title">{meeting['title']}</div>
#                         </div>
#                         """, unsafe_allow_html=True)
#         else:
#             st.info("No meetings to display")
        
#         # Color legend
#         st.markdown("---")
#         st.markdown("### 🎨 Color Legend")
        
#         legend_cols = st.columns(5)
#         legend_cols[0].markdown('<span style="display:inline-block;width:16px;height:16px;background:#161b22;border:1px solid #444;margin-right:8px;"></span>**0 meetings** - Free day', unsafe_allow_html=True)
#         legend_cols[1].markdown('<span style="display:inline-block;width:16px;height:16px;background:#0e4429;margin-right:8px;"></span>**1-2 meetings** - Light', unsafe_allow_html=True)
#         legend_cols[2].markdown('<span style="display:inline-block;width:16px;height:16px;background:#006d32;margin-right:8px;"></span>**3-4 meetings** - Moderate', unsafe_allow_html=True)
#         legend_cols[3].markdown('<span style="display:inline-block;width:16px;height:16px;background:#26a641;margin-right:8px;"></span>**5-6 meetings** - Busy', unsafe_allow_html=True)
#         legend_cols[4].markdown('<span style="display:inline-block;width:16px;height:16px;background:#39d353;margin-right:8px;"></span>**7+ meetings** - Very busy', unsafe_allow_html=True)


# except Exception as e:
#     st.error(f"❌ Error loading heatmap: {e}")
#     st.info("Make sure you're authenticated with Google Calendar")

































import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta
import pytz
import calendar as cal_module
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scheduler.google_calendar import get_calendar_service

st.set_page_config(page_title="Calendar Heatmap", page_icon="", layout="wide")

LOCAL_TZ = pytz.timezone('Asia/Kolkata')

# Custom CSS for dark, clean UI
st.markdown("""
<style>
    /* Dark theme */
    .stApp {
        background-color: #0e1117;
    }
    
    /* Header styling */
    .heatmap-header {
        text-align: center;
        padding: 20px 0;
        margin-bottom: 30px;
    }
    
    .heatmap-title {
        font-size: 2.5rem;
        font-weight: 700;
        color: #ffffff;
        margin-bottom: 8px;
    }
    
    .heatmap-subtitle {
        font-size: 1.1rem;
        color: #8b92a8;
    }
    
    /* Metric cards */
    .metric-card {
        background: linear-gradient(135deg, #1e2130 0%, #262b3e 100%);
        border-radius: 12px;
        padding: 20px;
        border: 1px solid #2d3348;
        transition: transform 0.2s;
    }
    
    .metric-card:hover {
        transform: translateY(-2px);
        border-color: #4a5568;
    }
    
    .metric-label {
        font-size: 0.9rem;
        color: #8b92a8;
        margin-bottom: 8px;
        font-weight: 500;
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        color: #ffffff;
    }
    
    .metric-delta {
        font-size: 0.85rem;
        margin-top: 4px;
    }
    
    .metric-delta.positive {
        color: #10b981;
    }
    
    .metric-delta.negative {
        color: #ef4444;
    }
    
    .metric-delta.neutral {
        color: #8b92a8;
    }
    
    /* Calendar grid */
    .calendar-container {
        background: linear-gradient(135deg, #1e2130 0%, #262b3e 100%);
        border-radius: 16px;
        padding: 30px;
        border: 1px solid #2d3348;
        margin: 20px 0;
    }
    
    /* Insight cards */
    .insight-card {
        background: linear-gradient(135deg, #1e2130 0%, #262b3e 100%);
        border-radius: 12px;
        padding: 18px;
        border-left: 4px solid;
        margin: 10px 0;
    }
    
    .insight-warning {
        border-left-color: #f59e0b;
    }
    
    .insight-success {
        border-left-color: #10b981;
    }
    
    .insight-info {
        border-left-color: #3b82f6;
    }
    
    /* Day details */
    .day-detail {
        background: #1a1f2e;
        border-radius: 8px;
        padding: 12px 16px;
        margin: 8px 0;
        border-left: 3px solid #3b82f6;
    }
    
    .meeting-time {
        color: #8b92a8;
        font-size: 0.9rem;
    }
    
    .meeting-title {
        color: #ffffff;
        font-size: 1rem;
        font-weight: 500;
        margin-top: 4px;
    }
    
    /* Time slot bars */
    .time-bar {
        background: #1a1f2e;
        border-radius: 6px;
        padding: 8px 12px;
        margin: 6px 0;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }
    
    .time-label {
        color: #8b92a8;
        font-size: 0.9rem;
        min-width: 80px;
    }
    
    .time-bar-fill {
        height: 20px;
        border-radius: 4px;
        background: linear-gradient(90deg, #10b981, #059669);
        transition: width 0.3s;
    }
    
    .time-count {
        color: #ffffff;
        font-weight: 600;
        margin-left: 10px;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="heatmap-header">
    <div class="heatmap-title"> Calendar Heatmap</div>
    <div class="heatmap-subtitle">Visual overview of your meeting patterns</div>
</div>
""", unsafe_allow_html=True)

# Month selector
col1, col2, col3 = st.columns([2, 3, 2])
with col2:
    today = datetime.now(LOCAL_TZ)
    
    # Generate list of months: 6 months back + current + 6 months forward
    months = []
    
    # Add past 6 months
    for i in range(6, 0, -1):
        date = today - timedelta(days=30*i)
        months.append(date.strftime("%B %Y"))
    
    # Add current month
    months.append(today.strftime("%B %Y"))
    
    # Add next 6 months
    for i in range(1, 7):
        date = today + timedelta(days=30*i)
        months.append(date.strftime("%B %Y"))
    
    selected_month_str = st.selectbox(
        "📅 Select Month",
        months,
        index=6,  # Default to current month (middle of list)
        key="month_selector"
    )
    
    # Parse selected month
    selected_date = datetime.strptime(selected_month_str, "%B %Y")
    selected_date = LOCAL_TZ.localize(selected_date)

st.markdown("---")

# Function to fetch meetings for a month
def fetch_month_data(year, month):
    service = get_calendar_service()
    first_day = LOCAL_TZ.localize(datetime(year, month, 1, 0, 0, 0))
    last_day_num = cal_module.monthrange(year, month)[1]
    last_day = LOCAL_TZ.localize(datetime(year, month, last_day_num, 23, 59, 59))
    
    events_result = service.events().list(
        calendarId='primary',
        timeMin=first_day.isoformat(),
        timeMax=last_day.isoformat(),
        singleEvents=True,
        orderBy='startTime'
    ).execute()
    
    events = events_result.get('items', [])
    
    daily_meetings = {}
    meeting_details = {}
    hourly_counts = {}
    
    for event in events:
        if 'dateTime' in event['start']:
            start = datetime.fromisoformat(event['start']['dateTime'].replace('Z', '+00:00'))
            start_local = start.astimezone(LOCAL_TZ)
            date_key = start_local.date()
            hour_key = start_local.hour
            
            # Count meetings per day
            daily_meetings[date_key] = daily_meetings.get(date_key, 0) + 1
            
            # Count meetings per hour
            hourly_counts[hour_key] = hourly_counts.get(hour_key, 0) + 1
            
            # Store meeting details
            if date_key not in meeting_details:
                meeting_details[date_key] = []
            
            meeting_details[date_key].append({
                'title': event.get('summary', 'Untitled'),
                'start': start_local,
                'end': datetime.fromisoformat(event['end']['dateTime'].replace('Z', '+00:00')).astimezone(LOCAL_TZ)
            })
    
    return daily_meetings, meeting_details, hourly_counts

# Fetch current month data
try:
    with st.spinner(f"📊 Loading meetings for {selected_month_str}..."):
        daily_meetings, meeting_details, hourly_counts = fetch_month_data(
            selected_date.year, 
            selected_date.month
        )
        
        # Fetch previous month data for comparison
        prev_month_date = selected_date - timedelta(days=30)
        prev_daily_meetings, _, _ = fetch_month_data(
            prev_month_date.year,
            prev_month_date.month
        )
        
        # Create calendar heatmap
        month_cal = cal_module.monthcalendar(selected_date.year, selected_date.month)
        
        # Prepare data for heatmap
        z_data = []
        hover_text = []
        customdata = []
        
        # Define proper color thresholds
        def get_color_for_count(count):
            if count == 0:
                return 0
            elif count <= 2:
                return 0.25
            elif count <= 4:
                return 0.5
            elif count <= 6:
                return 0.75
            else:
                return 1.0
        
        for week in month_cal:
            week_counts = []
            week_hover = []
            week_dates = []
            for day_num in week:
                if day_num == 0:
                    week_counts.append(None)
                    week_hover.append("")
                    week_dates.append(None)
                else:
                    date_obj = datetime(selected_date.year, selected_date.month, day_num).date()
                    count = daily_meetings.get(date_obj, 0)
                    week_counts.append(count)
                    week_hover.append(f"{date_obj.strftime('%B %d, %Y')}<br>{count} meeting{'s' if count != 1 else ''}")
                    week_dates.append(date_obj)
            
            z_data.append(week_counts)
            hover_text.append(week_hover)
            customdata.append(week_dates)
        
        # Create heatmap with FIXED color scale
        fig = go.Figure(data=go.Heatmap(
            z=z_data,
            x=['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
            y=[f"Week {i+1}" for i in range(len(month_cal))],
            colorscale=[
                [0, '#161b22'],      # 0 meetings - dark
                [0.25, '#0e4429'],   # 1-2 meetings - light green
                [0.5, '#006d32'],    # 3-4 meetings - medium green  
                [0.75, '#26a641'],   # 5-6 meetings - bright green
                [1.0, '#39d353']     # 7+ meetings - very bright green
            ],
            hovertemplate='%{hovertext}<extra></extra>',
            hovertext=hover_text,
            showscale=True,
            colorbar=dict(
                title="Meetings",
                titleside="right",
                tickmode="linear",
                tick0=0,
                dtick=2
            ),
            zmin=0,
            zmax=max([x for row in z_data for x in row if x is not None], default=7)
        ))
        
        fig.update_layout(
            title=dict(
                text=f"📅 {selected_month_str}",
                font=dict(size=20, color='white'),
                x=0.5,
                xanchor='center'
            ),
            xaxis=dict(
                side='top',
                showgrid=False,
                zeroline=False,
                color='white'
            ),
            yaxis=dict(
                showgrid=False,
                zeroline=False,
                color='white',
                autorange='reversed'
            ),
            plot_bgcolor='#1e2130',
            paper_bgcolor='#1e2130',
            height=400,
            margin=dict(l=60, r=60, t=80, b=40),
            font=dict(color='white')
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Calculate metrics
        total_meetings = sum(daily_meetings.values())
        last_day_num = cal_module.monthrange(selected_date.year, selected_date.month)[1]
        free_days = last_day_num - len(daily_meetings)
        avg_per_day = total_meetings / last_day_num if last_day_num > 0 else 0
        
        # Previous month metrics
        prev_total = sum(prev_daily_meetings.values())
        prev_days = cal_module.monthrange(prev_month_date.year, prev_month_date.month)[1]
        prev_avg = prev_total / prev_days if prev_days > 0 else 0
        
        # Calculate changes
        meetings_change = total_meetings - prev_total
        meetings_pct = (meetings_change / prev_total * 100) if prev_total > 0 else 0
        avg_change = avg_per_day - prev_avg
        
        # Find busiest day
        if daily_meetings:
            busiest_date = max(daily_meetings, key=daily_meetings.get)
            busiest_count = daily_meetings[busiest_date]
            busiest_day_str = busiest_date.strftime('%A, %B %d, %Y')
        else:
            busiest_day_str = "No meetings"
            busiest_count = 0
        
        st.markdown("---")
        
        # Metrics row with comparison
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            delta_class = "positive" if meetings_change < 0 else "negative" if meetings_change > 0 else "neutral"
            delta_symbol = "↓" if meetings_change < 0 else "↑" if meetings_change > 0 else "→"
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">📊 Total Meetings</div>
                <div class="metric-value">{total_meetings}</div>
                <div class="metric-delta {delta_class}">{delta_symbol} {abs(meetings_change)} vs last month</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">🔥 Busiest Day</div>
                <div class="metric-value">{busiest_count}</div>
                <div class="metric-delta neutral">{busiest_date.strftime('%b %d') if daily_meetings else 'N/A'}</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">✨ Free Days</div>
                <div class="metric-value">{free_days}</div>
                <div class="metric-delta neutral">{(free_days/last_day_num*100):.0f}% of month</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            avg_delta_class = "positive" if avg_change < 0 else "negative" if avg_change > 0 else "neutral"
            avg_symbol = "↓" if avg_change < 0 else "↑" if avg_change > 0 else "→"
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">📈 Daily Average</div>
                <div class="metric-value">{avg_per_day:.1f}</div>
                <div class="metric-delta {avg_delta_class}">{avg_symbol} {abs(avg_change):.1f} vs last month</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # CHANGED: Time of Day Analysis with Insights in right column
        st.markdown("### ⏰ Peak Meeting Hours")
        
        if hourly_counts:
            # Create time slots (9am to 6pm)
            time_slots = range(9, 18)
            max_hour_count = max(hourly_counts.values()) if hourly_counts else 1
            
            col1, col2 = st.columns([2, 1])
            
            with col1:
                for hour in time_slots:
                    count = hourly_counts.get(hour, 0)
                    bar_width = (count / max_hour_count * 100) if max_hour_count > 0 else 0
                    time_label = f"{hour % 12 if hour % 12 != 0 else 12}{'am' if hour < 12 else 'pm'}"
                    
                    st.markdown(f"""
                    <div class="time-bar">
                        <span class="time-label">{time_label}</span>
                        <div style="flex: 1; margin: 0 15px;">
                            <div class="time-bar-fill" style="width: {bar_width}%;"></div>
                        </div>
                        <span class="time-count">{count}</span>
                    </div>
                    """, unsafe_allow_html=True)
            
            with col2:
                # Peak Hour Card
                if hourly_counts:
                    peak_hour = max(hourly_counts, key=hourly_counts.get)
                    peak_count = hourly_counts[peak_hour]
                    peak_label = f"{peak_hour % 12 if peak_hour % 12 != 0 else 12}{'am' if peak_hour < 12 else 'pm'}"
                    
                    st.markdown(f"""
                    <div class="insight-card insight-info">
                        <strong>🔥 Peak Hour</strong><br>
                        <span style="font-size: 1.5rem; color: #10b981;">{peak_label}</span><br>
                        <span style="color: #8b92a8;">{peak_count} meetings</span>
                    </div>
                    """, unsafe_allow_html=True)
                
                # MOVED: Insights section to right column
                st.markdown("### 🧠 Insights")
                
                if daily_meetings:
                    st.markdown(f"""
                    <div class="insight-card insight-info">
                        <strong>🔥 Busiest Day:</strong> {busiest_day_str} with {busiest_count} meeting{'s' if busiest_count != 1 else ''}
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Comparison insight
                    if meetings_pct != 0:
                        trend = "increased" if meetings_pct > 0 else "decreased"
                        trend_class = "warning" if meetings_pct > 0 else "success"
                        st.markdown(f"""
                        <div class="insight-card insight-{trend_class}">
                            <strong>📊 Monthly Trend:</strong> Your meetings {trend} by {abs(meetings_pct):.0f}% compared to {prev_month_date.strftime('%B')}
                        </div>
                        """, unsafe_allow_html=True)
                    
                    if avg_per_day > 3:
                        st.markdown(f"""
                        <div class="insight-card insight-warning">
                            <strong>⚠️ High Meeting Load:</strong> You're averaging {avg_per_day:.1f} meetings per day. Consider blocking focus time.
                        </div>
                        """, unsafe_allow_html=True)
                    elif avg_per_day < 1:
                        st.markdown(f"""
                        <div class="insight-card insight-success">
                            <strong>✅ Healthy Balance:</strong> You have good focus time with only {avg_per_day:.1f} meetings per day on average.
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.info(f"✨ No meetings scheduled in {selected_month_str}")
        else:
            st.info("No meeting time data available for this month")
        
        st.markdown("---")
        
        # Interactive Day Selector (unchanged)
        st.markdown("### 📅 View Meetings by Day")
        
        if daily_meetings:
            # Create list of days with meetings
            days_with_meetings = sorted(daily_meetings.keys(), reverse=True)
            day_options = [d.strftime('%A, %B %d') for d in days_with_meetings]
            
            selected_day_str = st.selectbox(
                "Select a day to view meetings:",
                ["Select a day..."] + day_options,
                key="day_selector"
            )
            
            if selected_day_str != "Select a day...":
                # Find the corresponding date
                selected_day = None
                for day in days_with_meetings:
                    if day.strftime('%A, %B %d') == selected_day_str:
                        selected_day = day
                        break
                
                if selected_day and selected_day in meeting_details:
                    meeting_count = daily_meetings[selected_day]
                    st.markdown(f"#### 📋 {meeting_count} Meeting{'s' if meeting_count != 1 else ''} on {selected_day_str}")
                    
                    for meeting in meeting_details[selected_day]:
                        time_str = f"{meeting['start'].strftime('%I:%M %p')} - {meeting['end'].strftime('%I:%M %p')}"
                        duration = (meeting['end'] - meeting['start']).total_seconds() / 60
                        st.markdown(f"""
                        <div class="day-detail">
                            <div class="meeting-time">🕐 {time_str} ({duration:.0f} minutes)</div>
                            <div class="meeting-title">{meeting['title']}</div>
                        </div>
                        """, unsafe_allow_html=True)
        else:
            st.info("No meetings to display")
        
        # Color legend
        st.markdown("---")
        st.markdown("### 🎨 Color Legend")
        
        legend_cols = st.columns(5)
        legend_cols[0].markdown('<span style="display:inline-block;width:16px;height:16px;background:#161b22;border:1px solid #444;margin-right:8px;"></span>**0 meetings** - Free day', unsafe_allow_html=True)
        legend_cols[1].markdown('<span style="display:inline-block;width:16px;height:16px;background:#0e4429;margin-right:8px;"></span>**1-2 meetings** - Light', unsafe_allow_html=True)
        legend_cols[2].markdown('<span style="display:inline-block;width:16px;height:16px;background:#006d32;margin-right:8px;"></span>**3-4 meetings** - Moderate', unsafe_allow_html=True)
        legend_cols[3].markdown('<span style="display:inline-block;width:16px;height:16px;background:#26a641;margin-right:8px;"></span>**5-6 meetings** - Busy', unsafe_allow_html=True)
        legend_cols[4].markdown('<span style="display:inline-block;width:16px;height:16px;background:#39d353;margin-right:8px;"></span>**7+ meetings** - Very busy', unsafe_allow_html=True)

except Exception as e:
    st.error(f"❌ Error loading heatmap: {e}")
    st.info("Make sure you're authenticated with Google Calendar")






































