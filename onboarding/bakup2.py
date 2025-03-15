import streamlit as st

# from streamlit_geolocation import streamlit_geolocation
import requests

# import pandas as pd
# import numpy as np
# import plotly.express as px
# import plotly.graph_objects as go
# from datetime import datetime, timedelta


# st.set_page_config(
#     page_title="Risk Assessment",
#     page_icon="⚽",
#     layout="wide",
#     initial_sidebar_state="auto",
# )


# def activity_risk_assessment_page():
#     # when location is not detected
#     # st.info(
#     #     "Location not detected. Please allow location access. Default location is set to `Shah Alam`."
#     # )
#     st.title("Activity Risk Assessment")
#     st.subheader("Is it safe for my child to participate in outdoor activities?")
#     st.subheader("⬅️Find out now!")

#     # Sidebar for user inputs
#     with st.sidebar:
#         st.header("Child Information")

#         # Child's asthma severity
#         asthma_severity = st.radio(
#             "Asthma Severity Level", ["Mild", "Moderate", "Severe"], index=1
#         )

# Activity type
# activity_type = st.selectbox(
#     "Type of Activity",
#     [
#         "Light (walking, slow cycling)",
#         "Moderate (jogging, playground)",
#         "Intense (sports, running)",
#     ],
# )

# Activity duration
# duration = st.slider("Activity Duration (minutes)", 15, 120, 30, step=15)

# st.write("Location")
# location = streamlit_geolocation()
# if browse cant retrieve coordinates
# if location.get("latitude") is None or location.get("longitude") is None:
#     # by default will just set it to Shah Alam
#     latitude, longitude = 3.09060700, 101.52959690

# def get_location():
#     response = requests.get("https://ipinfo.io/json")
#     data = response.json()

#     if "loc" in data:
#         lat, lon = data["loc"].split(",")
#         return float(lat), float(lon)
#     else:
#         return None

# def get_aqi():
#     api_key = "78d4dab9fd82b3952d79356efc7c1bd46763f540"
#     latitude, longitude = get_location()
#     url = (
#         f"http://api.waqi.info/feed/geo:{latitude};{longitude}/?token={api_key}"
#     )
#     response = requests.get(url)
#     data = response.json()
#     aqi = data["data"]["aqi"]
#     name = data["data"]["city"]["name"]

#     return aqi, name

# latitude, longitude = get_location()

# st.write(get_aqi())

#         st.divider()

#         # Button to get recommendations
#         get_recommendation = st.button("Get Recommendations", type="primary")

#     st.divider()
#     if get_recommendation:
#         st.header("Main content")
#         st.write("Lets go")
#         st.write(f"Location Detected: {get_aqi()}")


# activity_risk_assessment_page()


# import requests


# def get_location():
#     response = requests.get("https://ipinfo.io/json")
#     data = response.json()

#     if "loc" in data:
#         lat, lon = data["loc"].split(",")
#         return float(lat), float(lon)
#     else:
#         return None


# latitude, longitude = get_location()
# st.write(latitude, longitude)


# def get_aqi(lat, lon, api_key="78d4dab9fd82b3952d79356efc7c1bd46763f540"):
#     url = f"http://api.waqi.info/feed/geo:{lat};{lon}/?token={api_key}"
#     response = requests.get(url)
#     return response.json()


# st.write(get_aqi(latitude, longitude))


# import requests

# location = streamlit_geolocation()
# st.write(location)

# # if browse cant retrieve coordinates
# if location.get("latitude") is None or location.get("longitude") is None:
#     st.info("Location not detected. Please allow location access.")
#     st.info("Default location is set to 'Shah Alam'")
#     # by default will just set it to Shah Alam
#     latitude, longitude = 3.09060700, 101.52959690


# def get_aqi(lat, lon, api_key="78d4dab9fd82b3952d79356efc7c1bd46763f540"):
#     url = f"http://api.waqi.info/feed/geo:{lat};{lon}/?token={api_key}"
#     response = requests.get(url)
#     return response.json()


# st.write(get_aqi(latitude, longitude))

# lat = location["latitude"]
# st.write(lat)
