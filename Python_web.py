import streamlit as st
import pandas as pd
import matplotlib as plt
import numpy as np
import requests
from datetime import datetime, timedelta
import time

# Track last refresh time
if 'last_refresh' not in st.session_state:
    st.session_state['last_refresh'] = time.time()

seconds_since_refresh = int(time.time() - st.session_state['last_refresh'])
st.write(f"Time since last refresh: {seconds_since_refresh} seconds")

# Auto-refresh every 60 seconds
if seconds_since_refresh >= 60:
    st.session_state['last_refresh'] = time.time()
    st.rerun()

# Calculate the start and end dates for the last 24 hours
endDate = datetime.now().strftime('%Y-%m-%d')
startDate = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')

sensor = '6L5P'

url = "https://jonnyhigham.com/ENVS666/shared_api.php?sensor="+str(sensor)+"&startDate="+startDate+"&endDate="+endDate
response = requests.get(url)
data = response.json()
data = data['data']
df = pd.DataFrame(data)
sensor = '6L5P'
df['Timestamp'] = pd.to_datetime(df['Timestamp'])

filter_mask = df['Timestamp'].dt.time > pd.to_datetime('4:00').time()
filtered_df = df[filter_mask]

st.title("Sensor Reading")

current_reading = df['PM2.5'].iloc[-1]
st.subheader(f"Current Value: {current_reading:.2f}")

fig, ax = plt.subplots()
ax.plot(filtered_df['Timestamp'], filtered_df['PM2.5'])
ax.set_xlabel('Time')
ax.set_ylabel('Sensor Reading')
ax.set_title('Sensor 6L5P Oil Readings (Last 24 Hours)')
ax.grid(True, which='major', linestyle='-', linewidth='0.5', color='gray')
ax.tick_params(axis='x', rotation=45)
ax.axhline(y=current_reading, color='red', linestyle='--', label='Current Reading')
ax.legend()
ax.minorticks_on()
ax.grid(True, which='minor', linestyle=':', linewidth='0.5', color='lightgray')

st.pyplot(fig)
