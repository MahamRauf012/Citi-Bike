# ================================================================
# Streamlit Dashboard – Citi Bike Strategy Dashboard (New York)
# Achievement 2.6
# ================================================================

import streamlit as st
import pandas as pd
import numpy as np
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import os

# ---------------------- PAGE CONFIG -----------------------------
st.set_page_config(page_title='Citi Bike Strategy Dashboard', layout='wide')

# ---------------------- TITLE & INTRO ---------------------------
st.title("🚴 Citi Bike Strategy Dashboard – New York City")
st.markdown("""
This dashboard visualizes **Citi Bike trip data** and **daily temperatures** in New York.  
Use it to identify popular stations and analyze how weather impacts ridership.
""")

# ---------------------- LOAD DATA -------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("reduced_data_to_plot.csv")
    top20 = pd.read_csv("top20_station.csv")
    return df, top20

try:
    df, top20 = load_data()
except Exception as e:
    st.error("⚠️ Could not load CSV files. Please ensure both files are uploaded to your folder.")
    st.stop()

# ---------------------- BAR CHART -------------------------------
st.subheader("Top 20 Most Popular Start Stations in New York")

fig_bar = go.Figure(
    go.Bar(
        x=top20['start_station_name'],
        y=top20['value'],
        marker={'color': top20['value'], 'colorscale': 'Blues'}
    )
)
fig_bar.update_layout(
    title="Top 20 Start Stations – Citi Bike NYC",
    xaxis_title="Start Station Name",
    yaxis_title="Number of Trips",
    width=1000,
    height=600
)
st.plotly_chart(fig_bar, use_container_width=True)

# ---------------------- DUAL-AXIS LINE CHART --------------------
st.subheader("Daily Bike Rides vs Average Temperature")

fig_line = make_subplots(specs=[[{"secondary_y": True}]])
fig_line.add_trace(
    go.Scatter(
        x=df['date'],
        y=df['bike_rides_daily'],
        name='Daily Bike Rides',
        line=dict(color='blue', width=2)
    ),
    secondary_y=False
)
fig_line.add_trace(
    go.Scatter(
        x=df['date'],
        y=df['avgTemp'],
        name='Average Temperature (°C)',
        line=dict(color='red', width=2)
    ),
    secondary_y=True
)
fig_line.update_layout(
    title="Daily Bike Rides vs Average Temperature in NYC (2018)",
    xaxis_title="Date",
    yaxis_title="Bike Rides",
    width=1000,
    height=600,
    legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1)
)
st.plotly_chart(fig_line, use_container_width=True)

# ---------------------- KEPLER MAP ------------------------------
st.subheader("🗺️ Aggregated Citi Bike Trips Map")

path_to_html = "CitiBike_Trips_Aggregated.html"

if os.path.exists(path_to_html):
    with open(path_to_html, 'r', encoding='utf-8') as f:
        html_data = f.read()
    st.components.v1.html(html_data, height=1000)
else:
    st.info("ℹ️ Map file not found. Please add **CitiBike_Trips_Aggregated.html** to your folder for the map to display.")

# ---------------------- FOOTER ---------------------------------
st.markdown("---")
st.caption("Data Source: Citi Bike (2022) and NOAA Weather. Dashboard created by Maham Rauf for CareerFoundry Achievement 2.6.")

