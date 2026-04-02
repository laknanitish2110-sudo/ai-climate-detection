import streamlit as st
import joblib
import numpy as np
import requests
import pandas as pd
import time

# Load model
model = joblib.load('../model/climate_model.pkl')

st.set_page_config(page_title="AI Climate App", layout="wide")

st.title("🌍 AI Climate Detection System (LIVE + MAP + GRAPH)")

API_KEY = "4db5e702d67d10f7ad3140ea28293413"

city = st.text_input("📍 Enter City Name", "Hyderabad")

if st.button("🔍 Get Weather & Predict"):

    url = f"https://api.openweathermap.org/data/2.5/weather?q={city},IN&appid={API_KEY}&units=metric"

    data = requests.get(url).json()

    if str(data.get("cod")) != "200":
        st.error(f"❌ {data.get('message')}")
    else:
        temp = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        wind = data["wind"]["speed"]
        rain = data.get("rain", {}).get("1h", 0)

        lat = data["coord"]["lat"]
        lon = data["coord"]["lon"]

        # 📊 Weather display
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("🌡️ Temp", temp)
        col2.metric("💧 Humidity", humidity)
        col3.metric("🌬️ Wind", wind)
        col4.metric("🌧️ Rain", rain)

        # 🤖 AI Prediction
        input_data = np.array([[temp, humidity, wind, rain]])
        result = model.predict(input_data)
        st.success(f"🤖 Climate Condition: {result[0]}")

        # 🗺️ MAP
        st.subheader("🗺️ Location Map")
        map_data = pd.DataFrame({'lat': [lat], 'lon': [lon]})
        st.map(map_data)

        # 📈 LIVE GRAPH (simulate updates)
        st.subheader("📊 Live Temperature Trend")

        chart = st.line_chart()

        temp_list = []

        for i in range(10):  # simulate 10 updates
            new_temp = temp + np.random.uniform(-2, 2)
            temp_list.append(new_temp)

            df = pd.DataFrame(temp_list, columns=["Temperature"])
            chart.line_chart(df)

            time.sleep(1)