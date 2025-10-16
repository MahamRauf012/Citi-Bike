# ================================================================
# Streamlit Dashboard – Citi Bike Strategy Dashboard (New York)
# Achievement 2.7 (Final)
# ================================================================

import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image
import plotly.graph_objects as go
import os

# ---------------------- PAGE CONFIG -----------------------------
st.set_page_config(page_title='Citi Bike Strategy Dashboard', layout='wide')

# ---------------------- SIDEBAR MENU ----------------------------
page = st.sidebar.selectbox(
    "Navigate to section:",
    ["Intro Page",
     "Daily Trends",
     "Most Popular Stations",
     "Interactive Map",
     "Recommendations"]
)

# ---------------------- LOAD DATA -------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("JC-202204-citibike-tripdata.csv")
    df.columns = df.columns.str.lower().str.strip()

    # Convert time columns
    if "started_at" in df.columns:
        df["start_time"] = pd.to_datetime(df["started_at"], errors="coerce")
    elif "start_time" in df.columns:
        df["start_time"] = pd.to_datetime(df["start_time"], errors="coerce")

    df["date"] = pd.to_datetime(df["start_time"], errors="coerce").dt.date
    df["month"] = pd.to_datetime(df["start_time"], errors="coerce").dt.month

    month_to_season = {
        12: "Winter", 1: "Winter", 2: "Winter",
        3: "Spring", 4: "Spring", 5: "Spring",
        6: "Summer", 7: "Summer", 8: "Summer",
        9: "Fall", 10: "Fall", 11: "Fall"
    }
    df["season"] = df["month"].map(month_to_season)

    return df

try:
    df = load_data()
except Exception as e:
    st.error("⚠️ Could not load the main CSV file. Please make sure `JC-202204-citibike-tripdata.csv` is in your folder.")
    st.stop()

# ---------------------- INTRO PAGE ------------------------------
if page == "Intro Page":
    st.title("🚴 Citi Bike Strategy Dashboard – New York City")
    st.markdown("""
    This dashboard visualizes **Citi Bike trip data** for April 2022.  
    It identifies **usage trends**, **popular stations**, and includes an **interactive trip map**  
    to support operational and strategic planning.
    """)
    st.info("Use the sidebar to explore the different dashboard sections.")

    total_rides = len(df)
    unique_stations = df['start_station_name'].nunique() if 'start_station_name' in df.columns else 0

    c1, c2 = st.columns(2)
    c1.metric("Total Trips (April 2022)", f"{total_rides:,}")
    c2.metric("Unique Start Stations", f"{unique_stations:,}")

    st.markdown("---")
    st.markdown("📊 **Dashboard Sections:**")
    st.markdown("- Daily ridership trends")
    st.markdown("- Most popular start stations")
    st.markdown("- Interactive trip map")
    st.markdown("- Key insights and recommendations")

# ---------------------- DAILY TRENDS ----------------------------
elif page == "Daily Trends":
    st.header("📈 Daily Citi Bike Rides – April 2022")

    daily = df.groupby('date', as_index=False).size().rename(columns={'size': 'rides'})

    fig = go.Figure(
        go.Scatter(
            x=daily['date'],
            y=daily['rides'],
            mode='lines+markers',
            line=dict(color='royalblue'),
            name='Daily Rides'
        )
    )
    fig.update_layout(
        title="Daily Citi Bike Rides",
        xaxis_title="Date",
        yaxis_title="Number of Rides",
        height=450
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("""
    **Observation:**  
    Daily ridership fluctuates with clear weekday peaks, suggesting commuter-driven demand.
    Weekend drops likely indicate leisure-oriented use.
    """)

# ---------------------- MOST POPULAR STATIONS -------------------
elif page == "Most Popular Stations":
    st.header("🏙️ Top 20 Start Stations – April 2022")

    if 'start_station_name' in df.columns:
        df['count'] = 1
        top20 = df.groupby('start_station_name', as_index=False)['count'].sum().nlargest(20, 'count')

        fig_bar = go.Figure(
            go.Bar(
                x=top20['start_station_name'],
                y=top20['count'],
                marker_color='cornflowerblue'
            )
        )
        fig_bar.update_layout(
            title="Top 20 Most Popular Start Stations",
            xaxis_title="Station Name",
            yaxis_title="Number of Trips",
            height=550,
            margin=dict(b=160)
        )
        st.plotly_chart(fig_bar, use_container_width=True)

        st.markdown("""
        **Insight:**  
        A handful of key stations generate most trips —  
        highlighting where bike rebalancing and infrastructure expansion matter most.
        """)
    else:
        st.warning("The column 'start_station_name' is missing from the dataset.")

# ---------------------- INTERACTIVE MAP -------------------------
elif page == "Interactive Map":
    st.header("🗺️ Citi Bike Trip Map (Kepler.gl)")

    map_file = "Final_CitiBike_Map_2.5.html"
    if os.path.exists(map_file):
        with open(map_file, 'r', encoding='utf-8') as f:
            html_data = f.read()
        st.components.v1.html(html_data, height=900)
    else:
        st.error("Map file not found. Please make sure `Final_CitiBike_Map_2.5.html` is in your folder.")

# ---------------------- RECOMMENDATIONS -------------------------
else:
    st.header("✅ Conclusions & Recommendations")
    st.markdown("""
    ### Key Takeaways
    1. **High-Demand Stations:** Downtown and near-waterfront areas drive the highest ridership.  
    2. **Seasonality:** Bike usage rises sharply between May and October, suggesting seasonal rebalancing.  
    3. **Operational Insight:** Reduce active bikes by ~25% during winter to lower logistics costs.  
    4. **Expansion Strategy:** Add docking stations near top 10 start stations and improve availability tracking.  
    5. **Next Step:** Integrate live data for real-time demand prediction and optimization.
    """)

    st.success("🎉 Dashboard completed – ready for presentation!")
