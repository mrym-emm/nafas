import streamlit as st
import time
import requests
import os
import pandas as pd
import plotly as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="NAFAS", page_icon="🍃", layout="wide", initial_sidebar_state="auto"
)


## to load css file for home screen animation
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
        <h4>because every child deserves the chance to breathe</h4>

    </div>


    """,
    unsafe_allow_html=True,
)


# give delay
time.sleep(5)

# the api token to retireve real time data
API_TOKEN = "78d4dab9fd82b3952d79356efc7c1bd46763f540"

# all available station ids, hardcoded, retrieved from aqicn website
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


st.markdown(
    """
    <div class="prompt-outside">
        <p>Real Time Air Quality Monitoring</p>
        <h3>Should 👨‍👩‍👧‍👦👨‍👩‍👧 go out today?</h3>
        <h3>⬇️Select a state below⬇️</h3>
        
    </div>

    """,
    unsafe_allow_html=True,
)


def get_aqi_data(station_id):
    """fetch complete air quality data from API and extract key metrics"""
    url = f"https://api.waqi.info/feed/@{station_id}/?token={API_TOKEN}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        if data.get("status") == "ok":
            # extract the aqi, temp and humidity data
            aqi = data["data"]["aqi"]
            temperature = data["data"].get("iaqi", {}).get("t", {}).get("v", "N/A")
            humidity = data["data"].get("iaqi", {}).get("h", {}).get("v", "N/A")

            pm10 = (
                data["data"]
                .get("forecast", {})
                .get("daily", {})
                .get("pm10", [{}])[0]
                .get("avg", "N/A")
            )

            pm25 = (
                data["data"]
                .get("forecast", {})
                .get("daily", {})
                .get("pm25", [{}])[0]
                .get("avg", "N/A")
            )

            o3 = (
                data["data"]
                .get("forecast", {})
                .get("daily", {})
                .get("o3", [{}])[0]
                .get("avg", "N/A")
            )

            # return all the extracted data
            return aqi, temperature, humidity, pm25, pm10, o3
        else:
            return ("Invalid station ID or no data available.",)
    else:
        return ("Error fetching data.",)


# returns the card color based on aqi. will only consider 3 since malaysia rarely above 100
def get_aqi_color(aqi):

    try:
        aqi_value = int(aqi)
        if aqi_value <= 50:
            return "#6BBF59"  # green is okay
        elif aqi_value <= 100:
            return "#FFBF00"  # yello is moderate
        else:
            return "#7E0023"  # marron - Hazardous
    except (ValueError, TypeError):
        return "#E7CD78"  # will return default card color(gold) if aqi is NA/cant be retirevd


# all states and city data to correspond to aqi
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

# cities dictionary to link to state list. redundant but it works
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


# ensuring session state exist
if "selected_state" not in st.session_state:
    st.session_state.selected_state = None
if "selected_city" not in st.session_state:
    st.session_state.selected_city = None


# necessary styling for button, couldnt make it work in css, this is for states
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
    font-size: 11px !important;
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

/* Card title styles - centered */
.card-title {
    text-align: center !important;
    margin: 0 !important;
    font-size: 18px !important;
    font-weight: bold !important;
}

/* Card value styles - centered and larger */
.card-value {
    text-align: center !important;
    margin: 0 !important;
    font-size: 28px !important;
    font-weight: bold !important;
}
</style>
""",
    unsafe_allow_html=True,
)

# creating columns to placed the button/cards so it looks organized
row1_cols = st.columns(6)

for i, state in enumerate(states[:6]):
    with row1_cols[i]:
        if st.button(state):
            st.session_state.selected_state = state

# displaying second row of states
row2_cols = st.columns(6)
for i, state in enumerate(states[6:]):
    with row2_cols[i]:
        # unique key for second row
        if st.button(state, key=f"btn_{state}"):
            st.session_state.selected_state = state


# if user select state, then show city in tht state via selectbox
if st.session_state.selected_state:
    state_cities = cities.get(st.session_state.selected_state, [])
    st.session_state.selected_city = st.selectbox(
        "Select Location:", state_cities, key="city_dropdown"
    )


if st.session_state.selected_city in station_id_dict:
    station_id = station_id_dict[st.session_state.selected_city]

    aqi, temperature, humidity, pm25, pm10, o3 = get_aqi_data(station_id)

    # create a three-column layout for AQI, Temperature, and Humidity
    col1, col2, col3 = st.columns(3)

    # Get color for aqi based on value
    aqi_color = get_aqi_color(aqi)

    # aqi card style with conditional message
    aqi_card_style = f"""
        <div style="
            padding: 20px;
            border-radius: 10px;
            background-color: {aqi_color};
            color: black;
            text-align: center;
            box-shadow: 0px 4px 8px rgba(0,0,0,0.2);
            height: 100%;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            ">
            <div class="card-title">AQI</div>
            <div class="card-value">{aqi}</div>
        </div>
    """

    # for simplicity, will only do warnings for 2 levels of aqi since thtat more common in malaysia
    if int(aqi) <= 49:
        for _ in range(2):
            st.write(" ")
        st.markdown(
            "<div style='text-align: center; font-family: \"Roboto Mono\", monospace;'>😷Generally safe, consider masks for sever asthma child!😷</div>",
            unsafe_allow_html=True,
        )

    elif int(aqi) > 50 and int(aqi) <= 100:

        for _ in range(2):
            st.write(" ")
        st.markdown(
            "<div style='text-align: center; font-family: \"Roboto Mono\", monospace;'>❗Children should limit prolong exposure!❗</div>",
            unsafe_allow_html=True,
        )

    # card_style for temp n humidity
    card_style = """
        <div style="
            padding: 20px;
            border-radius: 10px;
            background-color: #E7CD78;
            color: black;
            text-align: center;
            box-shadow: 0px 4px 8px rgba(0,0,0,0.2);
            height: 100%;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            ">
            <div class="card-title">{}</div>
            <div class="card-value">{}</div>
        </div>
    """

    # show cards for the temp, aqi and humidity
    with col1:
        st.markdown(card_style.format("🌤️ (°C)", temperature), unsafe_allow_html=True)

    with col2:
        st.markdown(aqi_card_style, unsafe_allow_html=True)
    with col3:
        st.markdown(card_style.format("💦 (%)", humidity), unsafe_allow_html=True)

    # add space
    for _ in range(1):
        st.write("")

    labels_pollutant = ["PM2.5", "PM10", "O\u2083"]
    pollutant_data = [pm25, pm10, o3]

    pollutant_df = pd.DataFrame(
        {"Pollutant": labels_pollutant, "Value": pollutant_data}
    )

    # create fig in plotly
    fig = go.Figure(
        data=go.Bar(
            x=labels_pollutant,
            y=pollutant_data,
            marker_color=["#FF9999", "#66B2FF", "#99FF99"],
        )
    )

    fig.update_layout(title="Pollutants in air")

    st.plotly_chart(fig)

    st.divider()

    st.subheader("⬇️Open Me⬇️")
    # adding expander to put explanation of above metrics
    with st.expander("How does this affect your child?"):

        info_df = pd.DataFrame(
            {
                "Factor": [
                    "**Temperature**",
                    "**Air Quality Index (AQI)**",
                    "**Humidity**",
                    "**PM 2.5 levels**",
                    "**PM 10 levels**",
                    "**O\u2083 levels**",
                ],
                "Explanation": [
                    "Hot weather can worsen asthma symptoms as higher temperatures can lead to increased respiratory issues. Heat can also increase air pollution levels, triggering asthma attacks in children.",
                    "AQI indicates the quality of air. Values below 50 are generally safe, `51-100` may affect sensitive groups, and values above `100` can impact your child's respiratory health and trigger asthma symptoms.",
                    "High humidity helps common allergens like dust mites and mold thrive, aggravating allergic asthma.",
                    "Fine particulate matter that can penetrate deep into the lungs. Levels above `12 μg/m³` can irritate airways and trigger asthma symptoms in children.",
                    "Larger particles that can irritate the throat and upper respiratory system. Can worsen asthma symptoms when levels exceed `50 μg/m³`.",
                    "Ground-level ozone that forms from pollutants reacting with sunlight. Can inflame airways and reduce lung function in children with asthma, especially during outdoor activities.",
                ],
            }
        )

        st.table(info_df)

        st.markdown(
            "The above information is <a href='https://www.researchgate.net/publication/343404673/figure/tbl1/AS:920630392287232@1596506798348/Air-quality-index-AQI-values-PM25-and-PM10-conc-color-codes-air-pollutant-level-of.png' target='_self'>sourced.</a>",
            unsafe_allow_html=True,
        )


else:
    # if user doesnt inser location will show this
    st.info("Please find your location!")

st.divider()

# add space
for _ in range(2):
    st.write("")
st.markdown("<b><u>More Links</u></b>", unsafe_allow_html=True)
# this creates a links
st.page_link("pages/Learn.py")
st.page_link("pages/Travel.py")
st.page_link("pages/Assess.py")
