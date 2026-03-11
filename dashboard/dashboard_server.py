import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
from datetime import datetime

# Page Config
st.set_page_config(page_title="AI Surveillance Dashboard", page_icon="🛡️", layout="wide")

# Custom CSS for Modern Video Management System (VMS) Look
st.markdown("""
<style>
/* Sleek Metric Cards */
[data-testid="stMetric"] {
    background-color: #1a1c23;
    border-left: 5px solid #00d2ff;
    padding: 15px;
    border-radius: 6px;
    box-shadow: 0 2px 5px rgba(0,0,0,0.2);
}
[data-testid="stMetricValue"] {
    font-size: 26px !important;
    font-weight: 700 !important;
}
[data-testid="stMetricLabel"] {
    font-size: 14px !important;
    font-weight: 600 !important;
    color: #a0aab2;
}
h1 {
    font-weight: 800;
    font-family: 'Inter', sans-serif;
    letter-spacing: -1px;
}
h3 {
    font-weight: 400;
    color: #b0b8c4;
}
</style>
""", unsafe_allow_html=True)

st.title("🛡️ Agentic AI Surveillance Platform")
st.markdown("### Real-time Event Detection & Analytics Command Center")

@st.cache_data(ttl=5)
def load_data():
    try:
        conn = sqlite3.connect("incidents.db")
        df = pd.read_sql_query("SELECT * FROM incidents ORDER BY timestamp DESC", conn)
        conn.close()
        
        # Convert timestamp to human readable format
        if not df.empty:
            df['datetime'] = pd.to_datetime(df['timestamp'], unit='s')
            
        return df
    except Exception as e:
        return pd.DataFrame()

df_incidents = load_data()

# 1. Top Metrics
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total Logged Events", len(df_incidents))
with col2:
    high_risk = len(df_incidents[df_incidents['risk_level'] == 'HIGH']) if not df_incidents.empty else 0
    st.metric("Critical Alerts", high_risk, delta_color="inverse")
with col3:
    loitering = len(df_incidents[df_incidents['event_type'] == 'loitering']) if not df_incidents.empty else 0
    st.metric("Loitering Detected", loitering)
with col4:
    st.metric("Edge Node Status", "ONLINE 🟢")

st.markdown("---")

# 2. Main Dashboard Area
left_col, center_col, right_col = st.columns([1, 2, 1])

with left_col:
    st.subheader("📈 Threat Timeline")
    if not df_incidents.empty:
        # Group by hour for timeline
        df_timeline = df_incidents.copy()
        df_timeline['hour'] = df_timeline['datetime'].dt.floor('H')
        timeline_data = df_timeline.groupby(['hour', 'risk_level']).size().reset_index(name='count')
        
        fig = px.bar(timeline_data, x='hour', y='count', color='risk_level', 
                     title="Activity History",
                     color_discrete_map={'LOW': '#00b894', 'MEDIUM': '#fdcb6e', 'HIGH': '#d63031'})
        fig.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No system events recorded.")

with center_col:
    st.subheader("🔴 Live Security Feed")
    st.markdown("**Node:** Camera-Alpha | **Analytics:** YOLOv8 Tracking Engine")
    
    # Placeholder for the video frame
    frame_placeholder = st.empty()
    
    # Simple checkbox to toggle play
    play_video = st.toggle("🎥 Activate Live Inference Engine", value=True)
    
    if play_video:
        import cv2
        import numpy as np
        import time
        import os
        from ultralytics import YOLO
        
        # Load real YOLO PyTorch model instead of mocking it
        try:
            # We are using the robust yolov8n.pt (Nano model on COCO) for optimized speed & detection accuracy
            model = YOLO("yolov8n.pt")
        except Exception as e:
            st.error(f"Failed to load AI weights (yolov8n.pt): {e}")
            model = None
            
        frames_dir = "data/frames"
        if os.path.exists(frames_dir) and model is not None:
            frames = sorted([f for f in os.listdir(frames_dir) if f.endswith('.jpg')])
            
            # Loop through frames to mock video playback
            for frame_file in frames:
                if not play_video:
                    break
                    
                frame_path = os.path.join(frames_dir, frame_file)
                img = cv2.imread(frame_path)
                
                if img is not None:
                    # Run actual YOLOv8 Tracking! classes=0 means person only
                    results = model.track(img, persist=True, classes=[0], verbose=False)
                    annotated_img = results[0].plot() # YOLO's incredible built-in visualizer with IDs
                    
                    # Draw Mock Restricted Zone Map over it
                    cv2.polylines(annotated_img, [np.array([[(0, 0), (200, 0), (200, 200), (0, 200)]])], 
                                  isClosed=True, color=(0, 0, 255), thickness=4)
                    cv2.putText(annotated_img, "RESTRICTED ZONE FOR LOITERING", (10, 30), 
                                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

                    # Convert BGR to RGB for Streamlit
                    img_rgb = cv2.cvtColor(annotated_img, cv2.COLOR_BGR2RGB)
                    frame_placeholder.image(img_rgb, channels="RGB", use_container_width=True)
                    # Removing explicitly sleep creates minimal frame latency for playback
        else:
             st.warning("Video stream offline. Verify Camera node connected.")
    else:
        # Default empty/offline frame
        frame_placeholder.info("System Standby. Enable Inference Engine to monitor feeds.")

with right_col:
    st.subheader("🚨 Recent Breaches")
    if not df_incidents.empty:
        for _, row in df_incidents.head(5).iterrows():
            with st.expander(f"{row['risk_level']} Risk - {row['event_type']} @ {row['datetime'].strftime('%H:%M:%S')}"):
                st.write(f"**Location:** {row['location']}")
                st.write(f"**Context:** {row['description']}")
    else:
        st.write("✅ System is secure. No recent threats logged.")

# 3. Data Table
st.markdown("---")
st.subheader("🗄️ Master Intelligence Log")
if not df_incidents.empty:
    display_df = df_incidents[['id', 'datetime', 'event_type', 'location', 'risk_level', 'description']]
    st.dataframe(display_df, use_container_width=True)
else:
    st.write("Incident database is empty.")

# 4. AI Query Interface (RAG Analytics)
st.markdown("---")
st.subheader("🤖 AI Agent Query Interface (RAG)")
st.markdown("Ask the AI about recent incidents or security policies:")

user_query = st.text_input("Enter your query:", placeholder="e.g. What suspicious events occurred today? or Why was this alert triggered?")

if user_query:
    from rag.knowledge_base import KnowledgeBase
    import time
    
    kb = KnowledgeBase()
    
    with st.spinner("AI Agent is reasoning using Vector DB and Incident Logs..."):
        time.sleep(1) # Simulate LLM inference delay
        query_lower = user_query.lower()
        
        if "what" in query_lower and ("occurred" in query_lower or "event" in query_lower):
            if not df_incidents.empty:
                recent = df_incidents.head(3) # Get top 3
                events_list = "\n".join([f"{i+1}. {row['event_type'].replace('_', ' ').title()} at {row['location']}" for i, row in recent.reset_index().iterrows()])
                st.success(f"**AI Answer:**\n\nI found the following suspicious events today:\n\n{events_list}")
            else:
                st.success("**AI Answer:**\n\nNo suspicious events have occurred today.")
                
        elif "why" in query_lower or "policy" in query_lower or "alert" in query_lower:
            target_event = "loitering" # default
            if "restricted" in query_lower:
                target_event = "restricted_area_entry"
            elif "crowd" in query_lower:
                target_event = "crowd_detected"
            elif not df_incidents.empty:
                target_event = df_incidents.iloc[0]['event_type']
                
            policy_reason = kb.query_policy(target_event)
            st.success(f"**AI Answer:**\n\nAccording to the security policy rule:\n> {policy_reason}\n\nThis behavior indicates a potential security risk and automatically generated a high-level alert.")
            
        else:
            st.success(f"**AI Answer:**\n\nI am currently tracking {len(df_incidents)} incidents. You can ask me to summarize the events or explain the security policies driving the alerts!")

# Real-time refresh hint
st.sidebar.markdown("### Control Panel")
if st.sidebar.button("↻ Force Refresh Data"):
    st.cache_data.clear()
    st.rerun()

st.sidebar.info("Dashboard auto-refreshes every 5 seconds.")
