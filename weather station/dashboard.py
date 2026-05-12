import streamlit as st
import serial
import pandas as pd
import time

# CONFIG
PORT = 'COM9'   # change if needed
BAUD = 115200

st.set_page_config(page_title="Weather Station", layout="wide")
st.title("🌦️ ESP32 Weather Station Dashboard")

# Connect serial (only once)
@st.cache_resource
def get_serial():
    return serial.Serial(PORT, BAUD, timeout=1)

ser = get_serial()

# Store data
if "data" not in st.session_state:
    st.session_state.data = pd.DataFrame(columns=["Temp", "Humidity"])

# Read ONE line per refresh (IMPORTANT)
line = ser.readline().decode(errors='ignore').strip()

if line:
    try:
        temp, hum = map(float, line.split(","))

        new_row = pd.DataFrame([[temp, hum]], columns=["Temp", "Humidity"])
        st.session_state.data = pd.concat([st.session_state.data, new_row])

        st.session_state.data = st.session_state.data.tail(50)

    except:
        pass

# UI
col1, col2 = st.columns(2)

if not st.session_state.data.empty:
    latest = st.session_state.data.iloc[-1]

    col1.metric("🌡️ Temperature (°C)", f"{latest['Temp']:.2f}")
    col2.metric("💧 Humidity (%)", f"{latest['Humidity']:.2f}")

    st.line_chart(st.session_state.data)

# Auto refresh every 2 seconds
time.sleep(2)
st.rerun()