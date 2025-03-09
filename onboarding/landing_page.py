import streamlit as st
import time
import requests

st.set_page_config(
    page_title="NAFAS", page_icon="🍃", layout="wide", initial_sidebar_state="collapsed"
)


# Load CSS
def load_css():
    with open("assets/styles_landing.css", "r") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


# apply css
load_css()

# landing page
st.markdown(
    """
    <div class="container">
        <h1>𖠋 N A F A S 𖠋</h1>
        <h4>because everyone deserves the chance to breathe</h4>

    </div>


    """,
    unsafe_allow_html=True,
)


# give delay
time.sleep(5)

# the api token to retireve real time data
API_TOKEN = "78d4dab9fd82b3952d79356efc7c1bd46763f540"

# all available station ids
station_id_dict = {
    "Pengerang": 0,
    "Kota Tinggi": 0,
    "Pasir Gudang": 0,
    "Larkin": 0,
    "Kluang": 0,
    "Batu Pahat": 0,
    "Segamat": 0,
    "Tangkak": 0,
    "Bandaraya Melaka": 0,
    "Alor Gajah": 0,
    "Port Dickson": 0,
    "Seremban": 0,
    "Nilai": 0,
    "Banting": 0,
    "Putrajaya": 0,
    "Klang": 0,
    "Shah Alam": 0,
    "Kuala Selangor": 0,
    "Petaling Jaya": 0,
    "Kuala Lumpur": 5780,
    "Batu Muda": 0,
    "Cheras": 0,
    "Rompin": 0,
    "Temerloh": 0,
    "Kuantan": 0,
    "Jerantut": 0,
    "Kemaman": 0,
    "Kuala Terengganu": 0,
    "Besut": 0,
    "Tanah Merah": 0,
    "Kota Bharu": 0,
    "Tanjong Malim": 0,
    "Ipoh": 0,
    "Taiping": 0,
    "Balik Pulau": 0,
    "Seberang Perai": 0,
    "Kulim": 0,
    "Sungai Petani": 0,
    "Alor Setar": 0,
    "Langkawi": 0,
    "Kangar": 0,
}

# st.write("Should you go out today?")
# station_id = st.text_input("Enter Station ID:", "")
st.markdown(
    """
    <div class="prompt-outside">
        <h3>Should 👦🏻👧🏽 go out today?</h3>
    </div>

    """,
    unsafe_allow_html=True,
)


def get_aqi(station_id):
    """fetch aqi, temp, wind from api"""
    url = f"https://api.waqi.info/feed/@{station_id}/?token={API_TOKEN}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        if data.get("status") == "ok":
            return data["data"]["aqi"]
        else:
            return "Invalid station ID or no data available."
    else:
        return "Error fetching data."


# using set better if im not updating
city = st.selectbox(label="Select", options=("None", "Kuala Lumpur"))

if city in station_id_dict:
    station_id = station_id_dict[city]
    aqi = get_aqi(station_id)
    # st.write(f"### AQI for Station {station_id}: {aqi}")
    st.write(aqi)
