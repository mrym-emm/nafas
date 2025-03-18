import streamlit as st
import datetime
from datetime import timedelta
import pandas as pd
import pydeck as pdk
import numpy as np
import math
import os
import pickle


st.set_page_config(
    page_title="🚗 Travel",
    page_icon="🍃",
    layout="wide",
    initial_sidebar_state="auto",
)


# setting styling to card input box
st.markdown(
    """
<style>
    /* Input box and control styles */
    .stDateInput > div > div,
    .stTextInput > div > div,
    .stSelectbox > div > div {
        background-color: rgba(255, 255, 255, 0.1) !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 8px !important;
        # color: white !important;
    }

    /* Fix for select dropdown */
    .stSelectbox > div[data-baseweb="select"] > div,
    .stSelectbox > div[data-baseweb="select"],
    .stSelectbox > div[data-baseweb="popover"],
    .stSelectbox > div[data-baseweb="menu"] {
        cursor: pointer !important;
        pointer-events: auto !important;
        z-index: 9999 !important;
    }

    .stSelectbox {
        z-index: 9999 !important;
        position: relative !important;
    }

    /* Force selectbox above map */
    div[data-testid="stAppViewContainer"] > div[data-testid="stVerticalBlock"] {
        z-index: 9999 !important;
        position: relative !important;
    }

    /* Make clickthrough map */
    [data-testid="stDeckGlJsonChart"] div {
        pointer-events: auto !important;
    }

    /* Map container style */
    .map-container {
        background-color: #2a2424 !important;
        border-radius: 15px !important;
        padding: 20px !important;
        margin-bottom: 20px !important;
        text-align: center !important;
        height: 400px !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        color: white !important;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3) !important;
    }

    /* Journey details box */
    .journey-details {
        background-color: rgba(255, 255, 255, 0.1);
        padding: 15px;
        border-radius: 8px;
        margin-top: 20px;
        margin-bottom: 20px;
    }

    .journey-details h4 {
        margin-top: 0;
        color: #E7CD78;
        margin-bottom: 15px;
    }

    .journey-details p {
        margin: 5px 0;
        padding: 0;
    }

    /* AQI indicator style */
    .aqi-indicator {
        width: 120px;
        height: 120px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 0 auto;
        font-weight: bold;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
    }

    /* AQI level colors */
    .aqi-good {background-color: #8BC34A;}
    .aqi-moderate {background-color: #FFC107;}
    .aqi-unhealthy {background-color: #FF5722;}

    /* Forecast panel */
    .forecast-panel {
        border-radius: 15px !important;
        padding: 20px !important;
        margin-top: 20px !important;
    }

    /* Title style - remove animation */
    .page-title {
        font-weight: 200 !important;
        text-align: center !important;
        letter-spacing: 5px !important;
        margin-bottom: 30px !important;
        opacity: 1 !important;
        animation: none !important;
    }

    /* Override global h1 animation */
    h1 {
        opacity: 1 !important;
        animation: none !important;
    }

    /* Title container with brown background */
    .title-container {
        background-color: #3a3232 !important; 
        border-radius: 15px !important;
        padding: 15px !important;
        margin-top: 30px !important; 
        margin-bottom: 30px !important;
        text-align: center !important;
        display: flex !important; 
        align-items: center !important; 
        justify-content: center !important;
        min-height: 80px !important; 
    }

    /* Title container h1 specific styles */
    .title-container h1 {
        margin: 0 !important; 
    }

    /* Button style - match Home page yellow color */
    .stButton > button {
        background-color: #E7CD78 !important;
        color: black !important;
        border: none !important;
        border-radius: 8px !important;
        font-family: "Roboto Mono", monospace !important;
        font-weight: 500 !important;
        padding: 10px 20px !important;
        transition: all 0.3s ease !important;
    }

    .stButton > button:hover {
        background-color: #EFBF04 !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2) !important;
    }

    # /* No animation for any text */
    # * {
    #     animation: none !important;
    #     transition: none !important;
    # }
</style>
""",
    unsafe_allow_html=True,
)


# initiailizze sessopm state when not clicked by user
if "search_submitted" not in st.session_state:
    st.session_state.search_submitted = False

if "selected_origin_state" not in st.session_state:
    st.session_state.selected_origin_state = "Select State"

if "selected_origin_city" not in st.session_state:
    st.session_state.selected_origin_city = "Select City"

if "selected_dest_state" not in st.session_state:
    st.session_state.selected_dest_state = "Select State"

if "selected_dest_city" not in st.session_state:
    st.session_state.selected_dest_city = "Select City"

# page titel
st.markdown(
    "<h1 class='page-title'>Travel Route & Air Quality</h1>", unsafe_allow_html=True
)

# city coordinates database - retrieved here (https://www.longitude-latitude-maps.com/)
# for demo purpose only seleceted location
city_coordinates = {
    "Alor Gajah": {
        "lat": 2.3805,
        "lon": 102.208,
    },
    "Bukit Jalil": {
        "lat": 3.0583,
        "lon": 101.6911,
    },
    "Cheras": {
        "lat": 3.0851,
        "lon": 101.7497,
    },
    "Ipoh": {
        "lat": 4.5975,
        "lon": 101.0901,
    },
    "Kemaman": {
        "lat": 4.2447,
        "lon": 103.4211,
    },
    "Kota Bharu": {
        "lat": 6.1254,
        "lon": 102.2381,
    },
    "Kuala Terengganu": {
        "lat": 5.3299,
        "lon": 103.137,
    },
    "Kuantan": {
        "lat": 3.825,
        "lon": 103.331,
    },
    "Langkawi": {
        "lat": 6.352,
        "lon": 99.7926,
    },
    "Perai": {
        "lat": 5.3841,
        "lon": 100.3973,
    },
    "Petaling Jaya": {
        "lat": 3.1073,
        "lon": 101.6067,
    },
    "Port Dickson": {
        "lat": 2.5246,
        "lon": 101.796,
    },
    "Putrajaya": {
        "lat": 2.9264,
        "lon": 101.6964,
    },
    "Seremban": {
        "lat": 2.7258,
        "lon": 101.9377,
    },
    "Shah Alam": {
        "lat": 3.0836,
        "lon": 101.5322,
    },
    "Sungai Petani": {
        "lat": 5.6497,
        "lon": 100.4877,
    },
    "Tangkak": {
        "lat": 2.2673,
        "lon": 102.5457,
    },
    "Temerloh": {
        "lat": 3.4496,
        "lon": 102.4211,
    },
}

# create column layout to set input and map
input_col, map_col = st.columns([1, 2])


# fx to create route path between two points
def create_path_data(origin, destination):
    if origin == "Select Location" or destination == "Select Location":
        return []

    origin_data = city_coordinates.get(origin)
    dest_data = city_coordinates.get(destination)

    if not origin_data or not dest_data:
        return []

    # get difference between points
    dx = dest_data["lon"] - origin_data["lon"]
    dy = dest_data["lat"] - origin_data["lat"]

    # determinining general direction and create waypoints
    num_waypoints = 6  # set number of intermediate points
    waypoints = []

    # add origin first
    waypoints.append({"lat": origin_data["lat"], "lon": origin_data["lon"]})

    # to make the path look like actual roads. the waypoints give it a jaggedy effect
    for i in range(1, num_waypoints):
        # calculate progress along the route (0-1)
        progress = i / num_waypoints

        # base position - direct interpolation
        base_lat = origin_data["lat"] + dy * progress
        base_lon = origin_data["lon"] + dx * progress

        # create road-like pattern by adding perpendicular offsets

        if i % 2 == 1:  # horizontal segment
            offset_lat = 0
            offset_lon = (0.1 * math.sin(progress * math.pi)) * (1 - progress)
        else:  # vertical segment
            offset_lat = (0.05 * math.sin(progress * math.pi)) * (1 - progress)
            offset_lon = 0

        waypoints.append({"lat": base_lat + offset_lat, "lon": base_lon + offset_lon})

    # add destination
    waypoints.append({"lat": dest_data["lat"], "lon": dest_data["lon"]})

    return waypoints


# malaysia map view
malaysia_view = pdk.ViewState(
    latitude=3.139,
    longitude=101.6869,
    zoom=8,
    pitch=0,  # set to 0 for flat map
    bearing=0,  # reset bearing to north to show how we typically see map
)


state_to_cities = {
    "Johor": ["Tangkak"],
    "Kedah": ["Langkawi", "Sungai Petani"],
    "Kelantan": ["Kota Bharu"],
    "Kuala Lumpur": ["Bukit Jalil", "Cheras"],
    "Melaka": ["Alor Gajah"],
    "Negeri Sembilan": ["Port Dickson", "Seremban"],
    "Pahang": ["Kuantan", "Temerloh"],
    "Penang": ["Perai"],
    "Perak": ["Ipoh"],
    "Putrajaya": ["Putrajaya"],
    "Selangor": ["Shah Alam", "Petaling Jaya"],
    "Terengganu": ["Kemaman", "Kuala Terengganu"],
}


# Input section
with input_col:
    st.markdown(
        "<h3 style='text-align: left;'>Plan Your Journey</h3>", unsafe_allow_html=True
    )
    st.subheader("Origin")
    col1, col2 = st.columns(2)

    # Initialize variables with default values
    selected_origin_city = "Select City"
    selected_dest_city = "Select City"

    with col1:
        with st.container():
            states = ["Select State"] + list(state_to_cities.keys())
            selected_origin_state = st.selectbox(
                "Starting Point (State)", options=states, key="origin_state_selectbox"
            )
            # Update session state
            st.session_state.selected_origin_state = selected_origin_state

    with col2:
        # select city
        if selected_origin_state != "Select State":
            cities = ["Select City"] + state_to_cities[selected_origin_state]
            selected_origin_city = st.selectbox(
                "Select City", options=cities, key="origin_city_selectbox"
            )
            st.session_state.selected_origin_city = selected_origin_city

    st.subheader("Destination")
    col3, col4 = st.columns(2)

    with col3:
        with st.container():
            states = ["Select State"] + list(state_to_cities.keys())
            selected_dest_state = st.selectbox(
                "End Point (State)", options=states, key="dest_state_selectbox"
            )
            # Update session state
            st.session_state.selected_dest_state = selected_dest_state

    with col4:
        # select city
        if selected_dest_state != "Select State":
            cities = ["Select City"] + state_to_cities[selected_dest_state]
            selected_dest_city = st.selectbox(
                "Select City", options=cities, key="dest_city_selectbox"
            )
            st.session_state.selected_dest_city = selected_dest_city

    # when teh webpage loads theres no city selected so this avoids error temporarily
    if selected_origin_city != "Select City":
        pass

    # Date selection
    travel_date = st.date_input("Date", datetime.date.today())

    # journey Details prompt when no destination is selected
    distance_text = "Select starting point and destination to see journey details."
    time_text = ""

    # only calculate distance if both origin and destination are selected
    if (
        selected_origin_city != "Select Location"
        and selected_dest_city != "Select Location"
        and selected_origin_city != selected_dest_city
    ):
        origin_data = city_coordinates.get(selected_origin_city)
        dest_data = city_coordinates.get(selected_dest_city)

        if origin_data and dest_data:
            # https://www.youtube.com/watch?v=TOTlkKMjQfw - used to calculate distance between 2 points
            # earth radius in km to used in formula
            R = 6371
            lat1, lon1 = math.radians(origin_data["lat"]), math.radians(
                origin_data["lon"]
            )
            lat2, lon2 = math.radians(dest_data["lat"]), math.radians(dest_data["lon"])

            dlon = lon2 - lon1
            dlat = lat2 - lat1

            a = (
                math.sin(dlat / 2) ** 2
                + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
            )
            c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
            distance = R * c

            # display journey details
            travel_time_hours = distance / 90
            travel_time_minutes = int(travel_time_hours * 90)

            distance_text = f"Distance: {distance:.1f} km"
            time_text = f"Est. Travel Time: {int(travel_time_hours)} hr {travel_time_minutes % 60} min"

    # display journey details
    st.markdown(
        f"""
    <div class="journey-details">
        <h5>Journey Details</h5>
        <p><strong>{distance_text}</strong></p>
        {f'<p><strong>{time_text}</strong></p>' if time_text else ''}
    </div>
    """,
        unsafe_allow_html=True,
    )

    # submit button
    if st.button("Check Air Quality"):
        st.session_state.search_submitted = True

# configuring map in its column
with map_col:
    # prepare map data
    map_data = []

    # ensuring origin always included when selected
    if (
        selected_origin_city != "Select Location"
        and selected_origin_city in city_coordinates
    ):
        data = city_coordinates[selected_origin_city]
        map_data.append(
            {
                "name": selected_origin_city,
                "lat": data["lat"],
                "lon": data["lon"],
                "type": "Origin",
                "label": "A",  # Add label A for origin
                "position": [data["lon"], data["lat"]],  # add position array format
            }
        )

    # ensuring destination always included when selected
    if (
        selected_dest_city != "Select Location"
        and selected_dest_city in city_coordinates
        and selected_dest_city != selected_origin_city
    ):
        data = city_coordinates[selected_dest_city]
        map_data.append(
            {
                "name": selected_dest_city,
                "lat": data["lat"],
                "lon": data["lon"],
                "type": "Destination",
                "label": "B",  # add label B for destination
                "position": [data["lon"], data["lat"]],  # add position array format
            }
        )

    # create dataframe for city markers
    locations = (
        pd.DataFrame(map_data)
        if map_data
        else pd.DataFrame(
            columns=["name", "lat", "lon", "aqi", "desc", "type", "label", "position"]
        )
    )

    # create route data if origin and destination are set and are different locations
    route_data = []
    if (
        selected_origin_city != "Select Location"
        and selected_dest_city != "Select Location"
        and selected_origin_city != selected_dest_city
    ):
        route_data = create_path_data(selected_origin_city, selected_dest_city)

    route_df = (
        pd.DataFrame(route_data)
        if route_data
        else pd.DataFrame(columns=["lat", "lon", "position"])
    )

    # this is the config for the circle marker
    circle_layer = pdk.Layer(
        "ScatterplotLayer",
        data=locations,
        get_position="position",
        get_radius=1500,  # size
        get_fill_color=[231, 205, 120, 220],  # color
        pickable=True,
        auto_highlight=True,
        stroked=True,
        get_line_color=[255, 255, 255],
        get_line_width=500,  # add border width fpr better visibility
        radius_scale=1,
        radius_min_pixels=5,
        radius_max_pixels=100,
    )

    # text layer for A(start) and B (end) font
    text_layer = pdk.Layer(
        "TextLayer",
        data=locations,
        get_position="position",
        get_text="label",  # use "A" and "B" labels
        get_color=[255, 87, 34, 255],  # color for label
        get_angle=0,
        get_text_anchor="middle",
        get_alignment_baseline="center",
        get_pixel_offset=[0, -13],
        billboard=True,
        size_scale=1,
        size_min_pixels=5,
        size_max_pixels=70,
    )

    # initialize layers list to order layer
    layers = []

    # add route line between origin and destination only when both are selected
    if (
        selected_origin_city != "Select Location"
        and selected_dest_city != "Select Location"
        and selected_origin_city != selected_dest_city
    ):
        # get waypoints for a more realistic driving route
        waypoints = create_path_data(selected_origin_city, selected_dest_city)

        if len(waypoints) >= 2:
            # convert waypoints to a path format
            path_data = []
            for i in range(len(waypoints) - 1):
                # create segments for each pair of waypoints
                path_data.append(
                    {
                        "path": [
                            [waypoints[i]["lon"], waypoints[i]["lat"]],
                            [waypoints[i + 1]["lon"], waypoints[i + 1]["lat"]],
                        ],
                        "color": [255, 152, 0],  # color for route
                    }
                )

            # create route path
            route_layer = pdk.Layer(
                "PathLayer",
                data=path_data,
                get_path="path",
                get_color="color",
                get_width=300,
                width_min_pixels=4,
                width_max_pixels=8,
                rounded=True,
                joint_rounded=True,
                cap_rounded=True,
                miter_limit=2,
                billboard=False,
                pickable=False,
            )

            # add route layer to the map
            layers.append(route_layer)

    # addomg all layers in correct order (route at bottom ->markers -> text)
    layers.append(circle_layer)
    layers.append(text_layer)

    # create tooltip
    tooltip = {
        "html": """
        <div style="padding: 12px; border-radius: 8px; box-shadow: 0 0 10px rgba(0,0,0,0.5);">
            <h3 style="margin-top: 0; color: #E7CD78;">{name}</h3>
            <p style="font-size: 16px;"><strong>AQI:</strong> {aqi}</p>
            <p>{desc}</p>
        </div>
        """,
        "style": {
            "backgroundColor": "rgba(42, 36, 36, 0.9)",
            "color": "white",
            "borderRadius": "8px",
            "padding": "15px",
            "fontFamily": "Roboto Mono, monospace",
            "fontSize": "14px",
        },
    }

    # display city count only if there are markers
    if not locations.empty:
        st.write(f"Displaying {len(map_data)} locations on map")

    # render map with flat view
    st.pydeck_chart(
        pdk.Deck(
            map_style="mapbox://styles/mapbox/dark-v10",
            initial_view_state=malaysia_view,
            layers=layers,
            tooltip=tooltip,
        )
    )

    # map instructions (for user to navigate map)
    st.markdown(
        """
    <div style="background-color: rgba(255, 255, 255, 0.1); padding: 10px; border-radius: 8px; font-size: 0.8em; margin-top: 10px;">
        <p style="margin: 0; text-align: center;">Click marker to view location details | Drag to move map | Double-click to zoom</p>
    </div>
    """,
        unsafe_allow_html=True,
    )

# forecast result panel (only displayed after submitting search)
if st.session_state.search_submitted:
    # get user destination name
    dest_name = st.session_state.get("selected_dest_city", "Select City")
    if dest_name == "Select City":
        st.error("Please select a specific city before checking air quality")
        st.session_state.search_submitted = False
        st.stop()

    # caching for speed
    @st.cache_resource
    def load_model(dest):
        try:
            # get the current directory and parent directory
            current_dir = os.path.dirname(os.path.abspath(__file__))
            parent_dir = os.path.dirname(current_dir)

            # mapping cities to their states
            city_to_state = {
                "alorgajah": "melaka",
                "bukitjalil": "kuala_lumpur",
                "cheras": "kuala_lumpur",
                "ipoh": "perak",
                "kemaman": "terengganu",
                "kotabharu": "kelantan",
                "kualaterengganu": "terengganu",
                "kuantan": "pahang",
                "langkawi": "kedah",
                "perai": "pulau_penang",
                "petalingjaya": "selangor",
                "portdickson": "negeri_sembilan",
                "putrajaya": "selangor",
                "seremban": "negeri_sembilan",
                "shahalam": "selangor",
                "sungaipetani": "kedah",
                "tangkak": "johor",
                "temerloh": "pahang",
            }

            # remove spaces in city name (to locate file later)
            dest_city = dest.lower().strip().replace(" ", "")

            # retrieve state name in city_to_state dictionary
            if dest_city not in city_to_state:
                raise ValueError(f"City '{dest_city}' not found in dataset mapping.")

            dest_state = city_to_state[dest_city]

            # generate the correct model filename based on the desttination
            model_filename = f"prophet_model_{dest_city}_{dest_state}.pkl"

            # to avoid error when location directory when deploying, list all path files
            possible_paths_aqi = [
                # current dir
                os.path.join(current_dir, model_filename),
                # All_States fodler in current dir
                os.path.join(current_dir, "All_States", model_filename),
                # parent directory
                os.path.join(parent_dir, model_filename),
                # All_States in parent directory
                os.path.join(parent_dir, "All_States", model_filename),
            ]

            # find and load model
            for path in possible_paths_aqi:
                if os.path.exists(path):
                    # st.write(f"Found model at: {path}")
                    with open(path, "rb") as file:
                        return pickle.load(file)

            # error exception
            raise FileNotFoundError(
                f"Couldn't find model file in any of the tried paths: {possible_paths_aqi}"
            )

        except Exception as e:
            st.error(f"Error loading model: {e}")
            return None

    # data from pickled mode
    dest = dest_name.replace(" ", "").lower().strip()
    # load pickled model
    model_aqi = load_model(dest)
    if model_aqi is None:
        st.error(f"Failed to load model of {dest_name}. Please check the model file.")
        st.stop()

    # ensuring target is within the date frame
    target_date = pd.to_datetime(travel_date)
    last_date = model_aqi.history["ds"].max()
    days_needed = (target_date - last_date).days + 1
    # display mdel info for user convenince
    st.markdown('<div class="forecast-panel">', unsafe_allow_html=True)
    st.info(
        f"Model loaded successfully. Historical data up to: {last_date.strftime('%Y-%m-%d')}"
    )

    # dataframe to store predcition (prophet functinoality)
    future_aqi = model_aqi.make_future_dataframe(periods=days_needed, freq="D")
    print(future_aqi.columns)

    # predict aqi
    forecast_aqi = model_aqi.predict(future_aqi)
    target_aqi = forecast_aqi[forecast_aqi["ds"] == target_date]

    if target_aqi.empty:
        st.error(f"Could not find forecast for {target_date.date()}.")
        st.stop()

    # retrieve AQI predictions
    predicted_aqi = target_aqi["yhat"].values[0]

    aqi_value = round(predicted_aqi, 0)

    # aqi and its risk level
    if aqi_value <= 50:
        aqi_class = "aqi-good"
        risk_level = "Low"
        risk_text = "Air quality is good, suitable for all outdoor activities."
    elif aqi_value <= 100:
        aqi_class = "aqi-moderate"
        risk_level = "Medium"
        risk_text = "Air quality is moderate, sensitive individuals may need to take precautions."
    else:
        aqi_class = "aqi-unhealthy"
        risk_level = "High"
        risk_text = "Air quality is poor, consider reducing outdoor activities."

    # st.markdown('<div class="forecast-panel">', unsafe_allow_html=True)
    st.markdown(
        f'<div class="title-container" style="margin-top: 70px; margin-left: auto; margin-right: auto;"><h1 class="page-title" style="color: white;">Air Quality Forecast in {dest_name}</h1></div>',
        unsafe_allow_html=True,
    )

    # column to arrange for aqi and forecast
    col1, col2, col3 = st.columns([1, 1, 1])

    with col2:
        st.markdown(
            f"""
        <div class="aqi-indicator {aqi_class}">
            <div>
                <div style="font-size: 14px; opacity: 0.8; text-align: center;">AQI</div>
                <div style="font-size: 32px;">{aqi_value}</div>
            </div>
        </div>
        <p style="text-align: center; margin-top: 10px; font-size: 16px;">Risk Level: {risk_level}</p>
        """,
            unsafe_allow_html=True,
        )

    # from user input, set it up for the next 5 days
    future_dates = [travel_date + timedelta(days=i) for i in range(5)]
    future_df = pd.DataFrame({"ds": future_dates})

    # use model to predict the future daytes
    forecast_aqi = model_aqi.predict(future_df)

    # extract AQI predictions for the next 5 days
    aqi_values = forecast_aqi["yhat"].round(0).astype(int).tolist()

    # format dates for display
    dates = [date.strftime("%m/%d") for date in future_dates]
    day_names = [date.strftime("%a") for date in future_dates]

    # create forecast timeline
    st.markdown(
        "<h3 style='text-align: center; margin: 30px 0 20px 0;'>5-Day Forecast</h3>",
        unsafe_allow_html=True,
    )

    forecast_cols = st.columns(5)

    for i in range(5):
        # colro for each aqi level
        if aqi_values[i] <= 50:
            aqi_color = "#8BC34A"  # green is good
        elif aqi_values[i] < 100:
            aqi_color = "#FFC107"  # yellow-moderate
        else:
            aqi_color = "#FF5722"  # red unhealthy

        with forecast_cols[i]:
            st.markdown(
                f"""
            <div style="text-align: center;">
                <div style="font-weight: bold;">{day_names[i]}</div>
                <div style="font-size: 12px; opacity: 0.8;">{dates[i]}</div>
                <div style="width: 50px; height: 50px; border-radius: 50%; background-color: {aqi_color}; 
                    color: white; display: flex; align-items: center; justify-content: center; 
                    margin: 10px auto; font-weight: bold;">
                    {aqi_values[i]}
                </div>
                
            </div>
            """,
                unsafe_allow_html=True,
            )
    for _ in range(2):
        st.write("")
    st.info("Disclaimer: These are simply predictions and for planning purposes.")
