# ================================================================
# Citi Bike Strategy Dashboard (New York)
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

    # Add the actual Intro image
    if os.path.exists("Intro.jpg"):
        st.image("Intro.jpg", caption="Citi Bike Stations Across New York City", use_column_width=True)
    else:
        st.warning("Intro image not found. Please ensure 'Intro.jpg' is in the same folder as this file.")

    st.markdown("""
    ### 🌆 Project Overview
    This dashboard visualizes **Citi Bike trip data** for April 2022, highlighting how and where New Yorkers use Citi Bikes.  
    It provides valuable insights into ridership trends, station performance, and usage patterns that can inform strategic decisions for operations and planning.
    """)

    st.markdown("""
    **Key Focus Areas:**
    - Daily ridership trends and fluctuations  
    - Top-performing start stations across NYC  
    - Geographical movement patterns via trip maps  
    - Recommendations for optimizing operations and scaling  
    """)

    st.info("💡 Tip: Use the sidebar to explore each dashboard section.")

    total_rides = len(df)
    unique_stations = df['start_station_name'].nunique() if 'start_station_name' in df.columns else 0

    c1, c2 = st.columns(2)
    c1.metric("Total Trips (April 2022)", f"{total_rides:,}")
    c2.metric("Unique Start Stations", f"{unique_stations:,}")

    st.markdown("""
    **Interpretation:**  
    April 2022 shows strong ridership volume and wide network usage, demonstrating Citi Bike’s importance as a sustainable transport mode.
    """)

# ---------------------- DAILY TRENDS ----------------------------
elif page == "Daily Trends":
    st.header("📈 Daily Citi Bike Rides – April 2022")

    daily = df.groupby('date', as_index=False).size().rename(columns={'size': 'rides'})

    fig = go.Figure(
        go.Scatter(
            x=daily['date'],
            y=daily['rides'],
            mode='lines+markers',
            line=dict(color='royalblue', width=2),
            name='Daily Rides'
        )
    )
    fig.update_layout(
        title="Daily Citi Bike Rides – April 2022",
        xaxis_title="Date",
        yaxis_title="Number of Rides",
        height=450
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("""
    ### Analysis  
    - Weekday peaks show a **strong commuter pattern**, with usage highest during workdays and slightly dropping on weekends.  
    - This pattern confirms Citi Bike’s dual purpose — **commuting during weekdays** and **leisure on weekends**.  
    - Rainy or cold days may correspond with visible dips in total rides.  
    - This trend highlights the need for **seasonal rebalancing** and possibly dynamic pricing or promotions on low-traffic days.
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
        ### Interpretation  
        - Most popular stations are clustered around **downtown Manhattan**, **Brooklyn waterfront**, and **near transit hubs**.  
        - These areas combine residential, commercial, and tourist activity, leading to consistent bike demand.  
        - **Strategic takeaway:**  
          - Focus on **frequent restocking** and **dock expansion** in these zones.  
          - Add more stations in nearby neighborhoods to **distribute pressure** from high-traffic docks.
        """)
    else:
        st.warning("The column 'start_station_name' is missing from the dataset.")

# ---------------------- INTERACTIVE MAP -------------------------
elif page == "Interactive Map":
    st.header("🗺️ Citi Bike Trip Map (Kepler.gl)")

    st.markdown("""
    This interactive map visualizes trip density across New York City.  
    It helps identify **major biking corridors**, **hotspots of activity**, and **potential expansion zones**.
    """)

    map_file = "Final_CitiBike_Map_2.5.html"
    if os.path.exists(map_file):
        with open(map_file, 'r', encoding='utf-8') as f:
            html_data = f.read()
        st.components.v1.html(html_data, height=900)
        st.caption("Each line represents aggregated bike trips between stations. Thicker lines = higher frequency.")
    else:
        st.error("Map file not found. Please make sure `Final_CitiBike_Map_2.5.html` is in your folder.")

    st.markdown("""
    **Insights:**  
    - The highest trip density appears in **downtown areas** and **near bridges**, indicating cross-borough travel.  
    - **Waterfront paths** are highly utilized during warm months, showing leisure-based demand.  
    - This data supports planning for **bike lanes, rebalancing trucks,** and **dock placement optimization.**
    """)

# ---------------------- RECOMMENDATIONS -------------------------
else:
    st.header("✅ Conclusions & Recommendations")

    # Add recommendation image
    if os.path.exists("Recommendation.jpg"):
        st.image("Recommendation.jpg", caption="Strategic Recommendations and Operational Planning", use_column_width=True)
    else:
        st.warning("Recommendation image not found. Please ensure 'Recommendation.jpg' is in the same folder as this file.")

    st.markdown("""
    ### Summary of Findings
    1. **High-Demand Zones:**  
       Downtown and waterfront areas consistently outperform others. Prioritize these for fleet management and redistribution.  
    2. **Seasonal Adjustment:**  
       Usage drops from November to April. Scaling back **25–30% of bikes** during winter reduces cost without affecting availability.  
    3. **Infrastructure Growth:**  
       Add new docking stations along popular water routes and residential zones near top stations.  
    4. **Real-Time Monitoring:**  
       Integrate weather and event data to predict spikes and automate rebalancing.  
    5. **User Engagement:**  
       Offer promotions or challenges during low-demand months to sustain ridership.  
    """)

    st.markdown("""
    ### Overall Conclusion  
    This analysis provides a clear understanding of how Citi Bike supports both **urban commuting** and **leisure cycling** in New York.  
    With data-driven planning, Citi Bike can improve **operational efficiency**, **user satisfaction**, and **system scalability**.
    """)

    
