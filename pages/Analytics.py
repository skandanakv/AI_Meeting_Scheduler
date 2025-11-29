import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import pytz
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scheduler.google_calendar import get_calendar_service

st.set_page_config(page_title="Meeting Analytics", page_icon="📊", layout="wide")

LOCAL_TZ = pytz.timezone('Asia/Kolkata')

# Custom CSS for dark, analytics-focused UI
st.markdown("""
<style>
    .stApp {
        background-color: #0e1117;
    }
    
    /* Hero Score Card */
    .hero-card {
        background: linear-gradient(135deg, #1e2130 0%, #262b3e 100%);
        border-radius: 16px;
        padding: 40px;
        text-align: center;
        border: 2px solid #2d3348;
        margin-bottom: 30px;
    }
    
    .score-value {
        font-size: 4rem;
        font-weight: 800;
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 10px 0;
    }
    
    .score-value.moderate {
        background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .score-value.poor {
        background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .score-label {
        font-size: 1.2rem;
        color: #8b92a8;
        margin-bottom: 10px;
    }
    
    .score-status {
        font-size: 1.5rem;
        font-weight: 600;
        color: #ffffff;
        margin-top: 10px;
    }
    
    .score-trend {
        font-size: 1rem;
        color: #8b92a8;
        margin-top: 5px;
    }
    
    /* Metric cards */
    .metric-card {
        background: linear-gradient(135deg, #1e2130 0%, #262b3e 100%);
        border-radius: 12px;
        padding: 24px;
        border: 1px solid #2d3348;
        height: 100%;
    }
    
    .metric-label {
        font-size: 0.9rem;
        color: #8b92a8;
        margin-bottom: 12px;
        font-weight: 500;
    }
    
    .metric-value {
        font-size: 2.5rem;
        font-weight: 700;
        color: #ffffff;
        margin-bottom: 8px;
    }
    
    .metric-subtitle {
        font-size: 0.85rem;
        color: #8b92a8;
    }
    
    /* Recommendation cards */
    .rec-card {
        background: linear-gradient(135deg, #1e2130 0%, #262b3e 100%);
        border-radius: 12px;
        padding: 20px;
        border-left: 4px solid;
        margin: 12px 0;
    }
    
    .rec-card.critical {
        border-left-color: #ef4444;
    }
    
    .rec-card.warning {
        border-left-color: #f59e0b;
    }
    
    .rec-card.success {
        border-left-color: #10b981;
    }
    
    .rec-card.info {
        border-left-color: #3b82f6;
    }
    
    .rec-title {
        font-weight: 600;
        font-size: 1.1rem;
        color: #ffffff;
        margin-bottom: 8px;
    }
    
    .rec-desc {
        color: #8b92a8;
        font-size: 0.95rem;
        margin-bottom: 8px;
    }
    
    .rec-action {
        color: #10b981;
        font-size: 0.9rem;
        font-weight: 500;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("# 📊 Meeting Analytics")
st.caption("Deep insights into your calendar patterns")

# Date range selector
col1, col2, col3 = st.columns([1, 1, 3])
with col1:
    days_back = st.selectbox("📅 Time Period", [7, 14, 30, 60, 90], index=2, key="period")
with col2:
    st.metric("Analyzing", f"Last {days_back} days", label_visibility="visible")

st.markdown("---")

# Fetch meetings
try:
    service = get_calendar_service()
    
    now = datetime.now(LOCAL_TZ)
    current_start = now - timedelta(days=days_back)
    previous_start = current_start - timedelta(days=days_back)
    
    with st.spinner("📊 Analyzing your calendar patterns..."):
        # Fetch current period
        events_result = service.events().list(
            calendarId='primary',
            timeMin=current_start.isoformat(),
            timeMax=now.isoformat(),
            singleEvents=True,
            orderBy='startTime'
        ).execute()
        
        current_events = events_result.get('items', [])
        
        # Fetch previous period for comparison
        prev_events_result = service.events().list(
            calendarId='primary',
            timeMin=previous_start.isoformat(),
            timeMax=current_start.isoformat(),
            singleEvents=True,
            orderBy='startTime'
        ).execute()
        
        prev_events = prev_events_result.get('items', [])
        
        # Process current period data
        meeting_data = []
        for event in current_events:
            if 'dateTime' in event['start']:
                start = datetime.fromisoformat(event['start']['dateTime'].replace('Z', '+00:00'))
                end = datetime.fromisoformat(event['end']['dateTime'].replace('Z', '+00:00'))
                duration = (end - start).total_seconds() / 60
                
                start_local = start.astimezone(LOCAL_TZ)
                end_local = end.astimezone(LOCAL_TZ)
                
                meeting_data.append({
                    'title': event.get('summary', 'Untitled'),
                    'start': start_local,
                    'end': end_local,
                    'date': start_local.date(),
                    'day_of_week': start_local.strftime('%A'),
                    'hour': start_local.hour,
                    'duration': duration,
                    'is_weekend': start_local.weekday() >= 5
                })
        
        df = pd.DataFrame(meeting_data)
        
        # Process previous period
        prev_meeting_count = 0
        prev_total_hours = 0
        for event in prev_events:
            if 'dateTime' in event['start']:
                prev_meeting_count += 1
                start = datetime.fromisoformat(event['start']['dateTime'].replace('Z', '+00:00'))
                end = datetime.fromisoformat(event['end']['dateTime'].replace('Z', '+00:00'))
                prev_total_hours += (end - start).total_seconds() / 3600
        
        if not df.empty:
            # Calculate core metrics
            total_meetings = len(df)
            total_hours = df['duration'].sum() / 60
            avg_duration = df['duration'].mean()
            meetings_per_day = total_meetings / days_back
            
            # Calculate back-to-back meetings
            df_sorted = df.sort_values('start')
            back_to_back = 0
            for i in range(len(df_sorted) - 1):
                gap = (df_sorted.iloc[i + 1]['start'] - df_sorted.iloc[i]['end']).total_seconds() / 60
                if gap < 15:
                    back_to_back += 1
            
            # Calculate focus blocks (gaps >= 2 hours)
            focus_blocks = []
            for i in range(len(df_sorted) - 1):
                gap_minutes = (df_sorted.iloc[i + 1]['start'] - df_sorted.iloc[i]['end']).total_seconds() / 60
                if gap_minutes >= 120:
                    focus_blocks.append(gap_minutes / 60)
            
            focus_block_count = len(focus_blocks)
            focus_hours = sum(focus_blocks)
            
            # Calculate fragmentation index
            daily_segments = df.groupby('date').size()
            fragmentation = daily_segments.mean() if len(daily_segments) > 0 else 0
            
            # Weekend meetings
            weekend_meetings = df[df['is_weekend']].shape[0]
            
            # Calculate Calendar Health Score (0-100)
            # Lower is better: fewer meetings, more focus time, less fragmentation
            meeting_load_score = min((meetings_per_day / 8) * 100, 100)  # 8+ meetings/day = 100 (worst)
            back_to_back_score = min((back_to_back / total_meetings) * 100, 100)
            fragmentation_score = min((fragmentation / 6) * 100, 100)  # 6+ segments = 100 (worst)
            focus_score = max(100 - (focus_block_count / days_back * 20) * 100, 0)  # Less focus blocks = worse
            
            health_score = 100 - ((meeting_load_score + back_to_back_score + fragmentation_score + focus_score) / 4)
            health_score = max(0, min(100, health_score))
            
            # Determine status
            if health_score >= 70:
                status = "Healthy"
                status_class = ""
            elif health_score >= 40:
                status = "Moderate"
                status_class = "moderate"
            else:
                status = "Overloaded"
                status_class = "poor"
            
            # Calculate trend
            prev_avg = prev_meeting_count / days_back if days_back > 0 else 0
            meeting_change = meetings_per_day - prev_avg
            change_pct = (meeting_change / prev_avg * 100) if prev_avg > 0 else 0
            trend_symbol = "↑" if change_pct > 0 else "↓" if change_pct < 0 else "→"
            
            # HERO CARD - Calendar Health Score
            st.markdown(f"""
            <div class="hero-card">
                <div class="score-label">Calendar Health Score</div>
                <div class="score-value {status_class}">{health_score:.0f}/100</div>
                <div class="score-status">{status}</div>
                <div class="score-trend">{trend_symbol} {abs(change_pct):.0f}% vs previous {days_back} days</div>
            </div>
            """, unsafe_allow_html=True)
            
            # Key Metrics Row
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">⏰ Meeting Time</div>
                    <div class="metric-value">{total_hours:.1f}h</div>
                    <div class="metric-subtitle">{(total_hours / (days_back * 8) * 100):.0f}% of work time</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">🎯 Focus Blocks</div>
                    <div class="metric-value">{focus_block_count}</div>
                    <div class="metric-subtitle">{focus_hours:.1f}h available (2+ hrs)</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">🔗 Back-to-Back</div>
                    <div class="metric-value">{back_to_back}</div>
                    <div class="metric-subtitle">{(back_to_back / total_meetings * 100):.0f}% no breaks</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col4:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">📊 Fragmentation</div>
                    <div class="metric-value">{fragmentation:.1f}</div>
                    <div class="metric-subtitle">segments per day</div>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("---")
            
            # Meeting Trend Chart
            st.markdown("### 📈 Meeting Load Over Time")
            
            # Daily meeting counts
            daily_counts = df.groupby('date').size().reset_index(name='count')
            daily_counts['date'] = pd.to_datetime(daily_counts['date'])
            
            # Create complete date range
            date_range = pd.date_range(start=current_start.date(), end=now.date(), freq='D')
            complete_df = pd.DataFrame({'date': date_range})
            complete_df = complete_df.merge(daily_counts, on='date', how='left').fillna(0)
            
            fig = go.Figure()
            
            fig.add_trace(go.Scatter(
                x=complete_df['date'],
                y=complete_df['count'],
                mode='lines+markers',
                name='Meetings',
                line=dict(color='#10b981', width=3),
                marker=dict(size=6),
                fill='tozeroy',
                fillcolor='rgba(16, 185, 129, 0.1)'
            ))
            
            # Add average line
            avg_line = meetings_per_day
            fig.add_hline(y=avg_line, line_dash="dash", line_color="#f59e0b", 
                         annotation_text=f"Avg: {avg_line:.1f}", 
                         annotation_position="bottom right",
                         annotation=dict(font=dict(size=12, color='#f59e0b')))
            
            fig.update_layout(
                plot_bgcolor='#1e2130',
                paper_bgcolor='#1e2130',
                font=dict(color='white'),
                xaxis=dict(showgrid=False, title="Date"),
                yaxis=dict(showgrid=True, gridcolor='#2d3348', title="Meetings per Day"),
                height=350,
                margin=dict(l=10, r=80, t=10, b=10),
                hovermode='x unified'
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            st.markdown("---")
            
            # Two column layout for charts
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("### ⏱️ Duration Breakdown")
                
                # Categorize durations
                duration_bins = [0, 30, 60, 120, float('inf')]
                duration_labels = ['< 30 min', '30-60 min', '1-2 hrs', '2+ hrs']
                df['duration_category'] = pd.cut(df['duration'], bins=duration_bins, labels=duration_labels, right=False)
                
                duration_counts = df['duration_category'].value_counts().sort_index()
                
                fig2 = go.Figure(data=[go.Pie(
                    labels=duration_counts.index,
                    values=duration_counts.values,
                    hole=0.4,
                    marker=dict(colors=['#10b981', '#3b82f6', '#f59e0b', '#ef4444'])
                )])
                
                fig2.update_layout(
                    plot_bgcolor='#1e2130',
                    paper_bgcolor='#1e2130',
                    font=dict(color='white'),
                    height=300,
                    margin=dict(l=10, r=10, t=10, b=10),
                    showlegend=True
                )
                
                st.plotly_chart(fig2, use_container_width=True)
            
            with col2:
                st.markdown("### 📅 Weekly Pattern")
                
                day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
                day_counts = df['day_of_week'].value_counts().reindex(day_order, fill_value=0)
                
                fig3 = go.Figure(data=[go.Bar(
                    x=day_counts.index,
                    y=day_counts.values,
                    marker=dict(
                        color=day_counts.values,
                        colorscale='Blues',
                        showscale=False
                    ),
                    text=day_counts.values,
                    textposition='outside'
                )])
                
                fig3.update_layout(
                    plot_bgcolor='#1e2130',
                    paper_bgcolor='#1e2130',
                    font=dict(color='white'),
                    xaxis=dict(showgrid=False, title=""),
                    yaxis=dict(showgrid=True, gridcolor='#2d3348', title="Meetings"),
                    height=300,
                    margin=dict(l=10, r=10, t=10, b=10)
                )
                
                st.plotly_chart(fig3, use_container_width=True)
            
            st.markdown("---")
            
            # Smart Recommendations
            st.markdown("### 💡 Smart Recommendations")
            
            recommendations = []
            
            # Back-to-back meetings
            if back_to_back > total_meetings * 0.3:
                recommendations.append({
                    'type': 'critical',
                    'title': '🚨 Too Many Back-to-Back Meetings',
                    'desc': f'You have {back_to_back} meetings with no breaks ({(back_to_back/total_meetings*100):.0f}% of total).',
                    'action': '→ Enable "Speedy Meetings" in Google Calendar (25/50 min default)'
                })
            
            # High meeting load
            if meetings_per_day > 5:
                recommendations.append({
                    'type': 'warning',
                    'title': '⚠️ High Meeting Load',
                    'desc': f'You\'re averaging {meetings_per_day:.1f} meetings per day ({(total_hours / (days_back * 8) * 100):.0f}% of work time).',
                    'action': '→ Review recurring meetings and decline non-essential invites'
                })
            
            # Fragmentation
            if fragmentation > 4:
                recommendations.append({
                    'type': 'warning',
                    'title': '📊 High Fragmentation',
                    'desc': f'Your day is split into {fragmentation:.1f} segments on average.',
                    'action': '→ Try batching meetings: Block 9am-12pm and 2pm-5pm for meetings'
                })
            
            # Low focus time
            if focus_block_count < days_back * 0.2:
                recommendations.append({
                    'type': 'warning',
                    'title': '🎯 Limited Focus Time',
                    'desc': f'Only {focus_block_count} blocks of 2+ hours available in {days_back} days.',
                    'action': '→ Block recurring "Focus Time" on your calendar'
                })
            
            # Weekend meetings
            if weekend_meetings > 0:
                recommendations.append({
                    'type': 'info',
                    'title': '📅 Weekend Meetings Detected',
                    'desc': f'You have {weekend_meetings} weekend meetings.',
                    'action': '→ Consider rescheduling for better work-life balance'
                })
            
            # Best day for focus
            lightest_day = day_counts.idxmin()
            lightest_count = day_counts.min()
            if lightest_count < meetings_per_day * 0.5:
                recommendations.append({
                    'type': 'success',
                    'title': f'✅ Best Focus Day: {lightest_day}',
                    'desc': f'{lightest_day}s average only {lightest_count} meetings.',
                    'action': f'→ Protect {lightest_day}s for deep work - decline new meeting requests'
                })
            
            # Long meetings
            long_meetings = df[df['duration'] > 120].shape[0]
            if long_meetings > total_meetings * 0.2:
                recommendations.append({
                    'type': 'info',
                    'title': '⏳ Many Long Meetings',
                    'desc': f'{long_meetings} meetings over 2 hours ({(long_meetings/total_meetings*100):.0f}%).',
                    'action': '→ Consider splitting into shorter sessions with breaks'
                })
            
            # Display recommendations
            for rec in recommendations:
                st.markdown(f"""
                <div class="rec-card {rec['type']}">
                    <div class="rec-title">{rec['title']}</div>
                    <div class="rec-desc">{rec['desc']}</div>
                    <div class="rec-action">{rec['action']}</div>
                </div>
                """, unsafe_allow_html=True)
            
            if not recommendations:
                st.success("🎉 Your calendar looks healthy! Keep up the good work.")
            
        else:
            st.info(f"📭 No meetings found in the last {days_back} days")

except Exception as e:
    st.error(f"❌ Error loading analytics: {e}")
    st.info("Make sure you're authenticated with Google Calendar")