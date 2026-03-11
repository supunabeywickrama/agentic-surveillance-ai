import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
from datetime import datetime

# Page Config
st.set_page_config(page_title="AI Surveillance Dashboard", page_icon="🛡️", layout="wide")
st.title("🛡️ Agentic AI Surveillance Platform")

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
    st.metric("Total Incidents Pipeline", len(df_incidents))
with col2:
    high_risk = len(df_incidents[df_incidents['risk_level'] == 'HIGH']) if not df_incidents.empty else 0
    st.metric("High Risk Alerts", high_risk, delta_color="inverse")
with col3:
    loitering = len(df_incidents[df_incidents['event_type'] == 'loitering']) if not df_incidents.empty else 0
    st.metric("Loitering Events", loitering)
with col4:
    st.metric("System Status", "Live 🟢")

st.markdown("---")

# 2. Main Dashboard Area
left_col, right_col = st.columns([2, 1])

with left_col:
    st.subheader("📈 Incident Timeline")
    if not df_incidents.empty:
        # Group by hour for timeline
        df_timeline = df_incidents.copy()
        df_timeline['hour'] = df_timeline['datetime'].dt.floor('H')
        timeline_data = df_timeline.groupby(['hour', 'risk_level']).size().reset_index(name='count')
        
        fig = px.bar(timeline_data, x='hour', y='count', color='risk_level', 
                     title="Incidents Over Time",
                     color_discrete_map={'LOW': 'green', 'MEDIUM': 'orange', 'HIGH': 'red'})
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No incidents recorded yet.")

with right_col:
    st.subheader("🚨 Recent Alerts")
    if not df_incidents.empty:
        for _, row in df_incidents.head(5).iterrows():
            with st.expander(f"{row['risk_level']} Risk - {row['event_type']} @ {row['datetime'].strftime('%H:%M:%S')}"):
                st.write(f"**Location:** {row['location']}")
                st.write(f"**Context:** {row['description']}")
    else:
        st.write("System is currently quiet.")

# 3. Data Table
st.markdown("---")
st.subheader("🗄️ Complete Incident Database")
if not df_incidents.empty:
    display_df = df_incidents[['id', 'datetime', 'event_type', 'location', 'risk_level', 'description']]
    st.dataframe(display_df, use_container_width=True)
else:
    st.write("No data available.")

# Real-time refresh hint
st.sidebar.markdown("### Control Panel")
if st.sidebar.button("↻ Force Refresh Data"):
    st.cache_data.clear()
    st.rerun()

st.sidebar.info("Dashboard auto-refreshes every 5 seconds.")
