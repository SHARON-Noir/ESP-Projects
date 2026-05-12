import streamlit as st
import serial
import pandas as pd
import time

# CONFIG
PORT = 'COM9'   # change if needed
BAUD = 115200

st.set_page_config(page_title="Weather Station", layout="wide")

st.title("🌦️ ESP32 Weather Station Dashboard")

# Connect serial
@st.cache_resource
def get_serial():
    return serial.Serial(PORT, BAUD, timeout=1)

ser = get_serial()

# Data storage
if "data" not in st.session_state:
    st.session_state.data = pd.DataFrame(columns=["Temp", "Humidity"])

# UI placeholders
temp_box = st.empty()
hum_box = st.empty()
chart = st.empty()

# Start loop
while True:
    try:
        line = ser.readline().decode().strip()

        if line:
            temp, hum = map(float, line.split(","))

            # Update dataframe
            new_row = pd.DataFrame([[temp, hum]], columns=["Temp", "Humidity"])
            st.session_state.data = pd.concat([st.session_state.data, new_row])

            # Keep last 50 values
            st.session_state.data = st.session_state.data.tail(50)

            # Display metrics
            temp_box.metric("Temperature (°C)", f"{temp:.2f}")
            hum_box.metric("Humidity (%)", f"{hum:.2f}")

            # Display chart
            chart.line_chart(st.session_state.data)

        time.sleep(1)

    except:
        pass