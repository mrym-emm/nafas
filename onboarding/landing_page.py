import streamlit as st
import time
import requests

import os

st.set_page_config(
    page_title="NAFAS", page_icon="🍃", layout="wide", initial_sidebar_state="collapsed"
)



current_dir = os.path.dirname(os.path.abspath(__file__))
css_path = os.path.join(current_dir, "styles_landing.css")

with open(css_path, "r") as f:
    css = f.read()
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)

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
    "Pengerang": 9495,
    "Kota Tinggi": 2577,
    "Pasir Gudang": 2580,
    "Larkin": 2578,
    "Kluang": 9494,
    "Batu Pahat": 9493,
    "Segamat": 9492,
    "Tangkak": 10484,
    "Bandaraya Melaka": 2586,
    "Alor Gajah": 9491,
    "Port Dickson": 2589,
    "Seremban": 2590,
    "Nilai": 2588,
    "Banting": 2617,
    "Putrajaya": 10485,
    "Klang": 2619,
    "Shah Alam": 2621,
    "Kuala Selangor": 2618,
    "Petaling Jaya": 2620,
    "Bukit Jalil": 5780,
    "Batu Muda": 2625,
    "Cheras": 2626,
    "Rompin": 9496,
    "Temerloh": 9497,
    "Kuantan": 2592,
    "Jerantut": 2593,
    "Kemaman": 2622,
    "Kuala Terengganu": 2623,
    "Besut": 9498,
    "Tanah Merah": 2585,
    "Kota Bharu": 9556,
    "Tanjong Malim": 2598,
    "Ipoh": 5777,
    "Taiping": 2595,
    "Balik Pulau": 9490,
    "Seberang Perai": 2600,
    "Kulim": 9488,
    "Sungai Petani": 9488,
    "Alor Setar": 2581,
    "Langkawi": 2583,
    "Kangar": 2599,
}

# st.write("Should you go out today?")
# station_id = st.text_input("Enter Station ID:", "")
st.markdown(
    """
    <div class="prompt-outside">
        <p>Real Time Air Quality Monitoring</p>
        <h3>Should 👦🏻👧🏽 go out today?</h3>
        
    </div>

    """,
    unsafe_allow_html=True,
)


def get_aqi_data(station_id):
    """fetch aqi, temp, humidty from api"""
    url = f"https://api.waqi.info/feed/@{station_id}/?token={API_TOKEN}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        if data.get("status") == "ok":
            aqi = data["data"]["aqi"]
            temperature = data["data"].get("iaqi", {}).get("t", {}).get("v", "N/A")
            humidity = data["data"].get("iaqi", {}).get("h", {}).get("v", "N/A")
            return aqi, temperature, humidity
        else:
            return "Invalid station ID or no data available."
    else:
        return "Error fetching data."


states = [
    "Kuala Lumpur",
    "Selangor",
    "Penang",
    "Johor",
    "Perak",
    "Negeri Sembilan",
    "Pahang",
    "Kelantan",
    "Terengganu",
    "Melaka",
    "Perlis",
    "Kedah",
]

cities = {
    "Johor": [
        "Batu Pahat",
        "Kluang",
        "Kota Tinggi",
        "Larkin",
        "Pengerang",
        "Pasir Gudang",
        "Segamat",
        "Tangkak",
    ],
    "Melaka": ["Alor Gajah", "BandarRaya Melaka"],
    "Negeri Sembilan": ["Nilai", "Port Dickson", "Seremban"],
    "Selangor": [
        "Banting",
        "Kuala Selangor",
        "Klang",
        "Petaling Jaya",
        "Shah Alam",
        "Putrajaya",
    ],
    "Kuala Lumpur": ["Batu Muda", "Bukit Jalil", "Cheras"],
    "Pahang": ["Jerantut", "Kuantan", "Rompin", "Temerloh"],
    "Terengganu": ["Besut", "Kemaman", "Kuala Terengganu"],
    "Kelantan": ["Kota Bharu", "Tanah Merah"],
    "Perak": ["Ipoh", "Taiping", "Tanjung Malim"],
    "Penang": ["Balik Pulau", "Seberang Perai"],
    "Kedah": ["Alor Setar", "Kulim", "Langkawi", "Sungai Petani"],
    "Perlis": ["Kangar"],
}


# Ensure session state variables exist
if "selected_state" not in st.session_state:
    st.session_state.selected_state = None
if "selected_city" not in st.session_state:
    st.session_state.selected_city = None

# create column based on state available
cols = st.columns(len(states))


# necessary styling for button, couldnt make it work in css
st.markdown(
    """
<style>
/* need to to brute force the styling because streamlits default always override */
.stButton > button,
.stButton > button div,
.stButton > button p,
.stButton > button div p,
.stButton > button > div,
.stButton button span,
div[data-testid="stHorizontalBlock"] div[data-testid="column"] div.stButton button,
div.stButton > button > div > p {
    font-size: 14px !important;
    line-height: 1.5 !important;
    font-family: "Roboto Mono", monospace !important;
}

/* equal spacing between buttons */
div[data-testid="stHorizontalBlock"] > div[data-testid="column"] {
    padding: 0 5px !important;
    display: flex !important;
    justify-content: center !important;
}

/* first column spacing */
div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:first-child {
    padding-left: 0 !important;
}

/* last column spacing */
div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:last-child {
    padding-right: 0 !important;
}

/* button container styling */
div.stButton {
    display: flex !important;
    justify-content: center !important;
    width: 100% !important;
}

/* color of button before click */
.stButton > button {
    width: 100% !important;
    margin: 0 !important;
    display: block !important;
    background-color: #E7CD78 !important;
    color: black !important;
    border: none !important;
    border-radius: 8px !important;
    transition: all 0.3s ease !important;
}

/* hover effect */
.stButton > button:hover {
    background-color: #EFBF04 !important;
    color: white !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2) !important;
}

/* effect when clicked */
.stButton > button:active {
    transform: translateY(0) !important;
    background-color: #D4B030 !important;
}
</style>
""",
    unsafe_allow_html=True,
)
# Create buttons for states
for i, state in enumerate(states):
    with cols[i]:
        if st.button(state):
            st.session_state.selected_state = state  # Store state in session

# If a state is selected, show city dropdown
if st.session_state.selected_state:
    state_cities = cities.get(st.session_state.selected_state, [])
    st.session_state.selected_city = st.selectbox(
        "Select Location:", state_cities, key="city_dropdown"
    )


if st.session_state.selected_city in station_id_dict:
    station_id = station_id_dict[st.session_state.selected_city]
    aqi, temperature, humidity = get_aqi_data(station_id)

    # Create a three-column layout for AQI, Temperature, and Humidity
    col1, col2, col3 = st.columns(3)

    # Styling for cards
    card_style = """
        <div style="
            padding: 20px;
            border-radius: 10px;
            background-color: #E7CD78;
            color: black;
            font-size: 18px;
            text-align: center;
            box-shadow: 0px 4px 8px rgba(0,0,0,0.2);
            ">
            <h3 style="margin: 0;">{}</h3>
            <p style="margin: 0; font-size: 24px; font-weight: bold;">{}</p>
        </div>
    """

    with col1:
        st.markdown(card_style.format("AQI", aqi), unsafe_allow_html=True)
    with col2:
        st.markdown(
            card_style.format("Temperature (°C)", temperature), unsafe_allow_html=True
        )
    with col3:
        st.markdown(card_style.format("Humidity (%)", humidity), unsafe_allow_html=True)
