# ================================
# Divvy Bikes Strategy Dashboard
# Created by Maham Rauf
# ================================

import streamlit as st
import pandas as pd
import numpy as np
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import os

# -------------------------------
# PAGE CONFIG
# -------------------------------
st.set_page_config(page_title="Divvy Bikes Strategy Dashboard", layout="wide")

st.title("🚴 Divvy Bikes Strategy Dashboard")
st.markdown("""
This dashboard visualizes key insights about Divvy Bike usage and trends.
It includes:
- The 20 most popular bike stations
- Temperature and ride frequency correlation
- Aggregated trip statistics and summary tables
""")

# -------------------------------
# LOAD DATA
# -------------------------------
st.header("📂 Loading Data")

# Change file names if needed to match your CSVs
try:
    trips = pd.read_csv("trips_weather.csv")
    stations = pd.read_csv("top20_station.csv")
    st.success("✅ Data loaded successfully!")
except FileNotFoundError:
    st.error("❌ Missing one or more CSV files in this folder.")
    st.stop()

# -------------------------------
# PREVIEW TABLES
# -------------------------------
st.subheader("📊 Data Preview")
st.write("### Trips & Weather Data")
st.dataframe(trips.head())

st.write("### Top 20 Stations Data")
st.dataframe(stations.head())

# -------------------------------
# BAR CHART — Most Popular Stations
# -------------------------------
st.header("🏙️ Top 20 Most Popular Bike Stations")

fig_bar = go.Figure(go.Bar(
    x=stations["start_station_name"],
    y=stations["value"],
    marker=dict(color=stations["value"], colorscale="Blues")
))
fig_bar.update_layout(
    title="Top 20 Most Popular Bike Stations in Chicago",
    xaxis_title="Start Station",
    yaxis_title="Number of Trips",
    height=600
)
st.plotly_chart(fig_bar, use_container_width=True)

# -------------------------------
# DUAL-AXIS LINE CHART — Bike Rides vs Temperature
# -------------------------------
st.header("🌡️ Temperature and Daily Bike Usage")

fig_line = make_subplots(specs=[[{"secondary_y": True}]])

fig_line.add_trace(
    go.Scatter(x=trips["date"], y=trips["trip_count"],
               name="Daily Bike Rides", line=dict(color="blue")),
    secondary_y=False
)

fig_line.add_trace(
    go.Scatter(x=trips["date"], y=trips["avgTemp"],
               name="Average Temperature", line=dict(color="red")),
    secondary_y=True
)

fig_line.update_layout(
    title="Daily Bike Rides and Average Temperature (2018)",
    height=500
)
fig_line.update_yaxes(title_text="Bike Rides", secondary_y=False)
fig_line.update_yaxes(title_text="Temperature (°C)", secondary_y=True)

st.plotly_chart(fig_line, use_container_width=True)

# -------------------------------
# SUMMARY TABLES
# -------------------------------
st.header("📈 Summary Statistics")

col1, col2 = st.columns(2)
with col1:
    st.subheader("Trips Summary")
    st.write(trips.describe())
with col2:
    st.subheader("Stations Summary")
    st.write(stations.describe())

# -------------------------------
# FOOTER
# -------------------------------
st.markdown("---")
st.markdown("📅 **Data Source:** Divvy Bikes (via Kaggle) & NOAA | Created by **Maham Rauf**")