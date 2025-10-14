
# ===============================================
# STREAMLIT DASHBOARD: Citi Bike Strategy Dashboard (New York)
# ===============================================

import streamlit as st
import pandas as pd
from plotly.subplots import make_subplots
import plotly.graph_objects as go

# ---------------------------
# PAGE CONFIGURATION
# ---------------------------
st.set_page_config(page_title='Citi Bike Strategy Dashboard', layout='wide')
st.title("🚲 Citi Bike Strategy Dashboard — New York City")
st.markdown("### Explore Citi Bike usage patterns, temperatures, and station popularity across New York City.")

# ---------------------------
# IMPORT DATA
# ---------------------------
df_top20 = pd.read_csv('top20_station.csv')
df_reduced = pd.read_csv('reduced_data_to_plot.csv')

# ---------------------------
# BAR CHART — Top 20 Stations
# ---------------------------
st.header("Top 20 Most Popular Citi Bike Stations")
fig_bar = go.Figure(
    go.Bar(
        x=df_top20['start_station_name'],
        y=df_top20['value'],
        marker={'color': df_top20['value'], 'colorscale': 'Blues'},
    )
)
fig_bar.update_layout(
    title='Top 20 Most Popular Citi Bike Stations in New York',
    xaxis_title='Start Stations',
    yaxis_title='Number of Trips',
    xaxis_tickangle=-45,
    height=600
)
st.plotly_chart(fig_bar, use_container_width=True)

# ---------------------------
# DUAL-AXIS LINE CHART — Trips vs Temperature
# ---------------------------
st.header("Daily Citi Bike Trips vs Average Temperature")
fig_line = make_subplots(specs=[[{"secondary_y": True}]])

# Primary Y (Bike rides)
fig_line.add_trace(
    go.Scatter(
        x=df_reduced['date'],
        y=df_reduced['bike_rides_daily'],
        mode='lines',
        name='Daily Bike Rides',
        line=dict(color='royalblue', width=2)
    ),
    secondary_y=False,
)

# Secondary Y (Temperature)
fig_line.add_trace(
    go.Scatter(
        x=df_reduced['date'],
        y=df_reduced['avgTemp'],
        mode='lines',
        name='Average Temperature (°C)',
        line=dict(color='firebrick', width=2, dash='dot')
    ),
    secondary_y=True,
)

fig_line.update_layout(
    title='Bike Usage and Temperature Trends (2022)',
    xaxis_title='Date',
    yaxis_title='Bike Rides',
    height=600,
    legend=dict(x=0.01, y=0.99)
)

fig_line.update_yaxes(title_text="Bike Rides", secondary_y=False)
fig_line.update_yaxes(title_text="Average Temperature (°C)", secondary_y=True)
st.plotly_chart(fig_line, use_container_width=True)

# ---------------------------
# MAP PLACEHOLDER — Kepler Map
# ---------------------------
st.header("Aggregated Citi Bike Trips in New York City")
st.markdown("*(Kepler.gl interactive map placeholder — upload your HTML map below to render)*")

uploaded_map = st.file_uploader("Upload your Kepler map HTML file", type=["html"])
if uploaded_map is not None:
    st.components.v1.html(uploaded_map.read(), height=800)
else:
    st.info("Please upload your Kepler map HTML file to display it here.")
