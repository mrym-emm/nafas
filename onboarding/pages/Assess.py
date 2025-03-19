import pandas as pd
import streamlit as st
import requests
import plotly.graph_objects as go



st.set_page_config(
    page_title="Risk Assessment",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="auto",
)

state_cities_dict = {
    "Kuala Lumpur": [
        "Kuala Lumpur",
        "Bukit Bintang",
        "Chow Kit",
        "Bangsar",
        "Mont Kiara",
        "Brickfields",
        "Cheras",
    ],
    "Selangor": [
        "Shah Alam",
        "Petaling Jaya",
        "Subang Jaya",
        "Klang",
        "Puchong",
        "Putrajaya",
        "Kota Damansara",
    ],
    "Terengganu": ["Kemaman"],
}
city_coordinates = {
    "Kuala Lumpur": {
        "lat": 3.140853,
        "lon": 101.693207,
    },
    "Bukit Bintang": {
        "lat": 3.146708,
        "lon": 101.711197,
    },
    "Chow Kit": {
        "lat": 3.165186,
        "lon": 101.6988038,
    },
    "Bangsar": {
        "lat": 3.13083,
        "lon": 101.66944,
    },
    "Kemaman": {
        "lat": 4.2193065,
        "lon": 103.4225158,
    },
    "Mont Kiara": {
        "lat": 3.1699988,
        "lon": 101.6521467,
    },
    "Brickfields": {
        "lat": 3.1288572,
        "lon": 101.6845528,
    },
    "Cheras": {
        "lat": 3.0991919,
        "lon": 101.7374229,
    },
    "Shah Alam": {
        "lat": 3.0739429,
        "lon": 101.5185278,
    },
    "Petaling Jaya": {
        "lat": 3.1073,
        "lon": 101.6067,
    },
    "Puchong": {
        "lat": 3.0342324,
        "lon": 101.6170345,
    },
    "Putrajaya": {
        "lat": 2.9264,
        "lon": 101.6964,
    },
    "Subang Jaya": {
        "lat": 3.051487,
        "lon": 101.5823339,
    },
    "Klang": {
        "lat": 3.0448394,
        "lon": 101.4447363,
    },
    "Kota Damansara": {
        "lat": 3.1536719,
        "lon": 101.593544,
    },
}

try:
    # getting current user aqi, pm2.5
    def get_aqi_city(city):
        # geo_url = f"https://nominatim.openstreetmap.org/search?city={city}&country=Malaysia&format=json"
        # response = requests.get(geo_url, headers={"User-Agent": "ActivityRiskApp"})
        # data = response.json()
        # lat, long = data[0].get("lat"), data[0].get("lon")
        lat = city_coordinates[city]["lat"]
        long = city_coordinates[city]["lon"]

        aqi_url = f"http://api.waqi.info/feed/geo:{lat};{long}/?token=78d4dab9fd82b3952d79356efc7c1bd46763f540"

        aqi_response = requests.get(aqi_url)
        aqi_data = aqi_response.json()

        aqi = aqi_data["data"]["aqi"]
        pm25 = (
            aqi_data["data"]
            .get("forecast", {})
            .get("daily", {})
            .get("pm25", [{}])[0]
            .get("avg", "N/A")
        )

        return aqi, pm25

    def activity_risk_assessment_page():
        st.markdown(
            """<h1 style="text-align:center;">Should my child go outside?</h1>""",
            unsafe_allow_html=True,
        )
        st.markdown(
            """<h2 style="text-align:center;"><span style="color: #FF4B4B;">Get Recommendation</span> now in sidebar!</h2>""",
            unsafe_allow_html=True,
        )

        st.divider()

        # create a placeholder in the main area for content that will show after rec button iz click
        main_content_placeholder = st.empty()

        with st.sidebar:
            st.subheader("Location")

            col1, col2 = st.columns(2)

            with col1:
                selected_state = ["Select State"] + list(state_cities_dict.keys())
                # so user can select available city
                select_location_state = st.selectbox(
                    "Select State", options=selected_state
                )

            with col2:
                # only get state when user select
                if select_location_state != "Select State":
                    # filter city based on the state selected above
                    cities_for_selected_state = state_cities_dict[select_location_state]
                    select_location_city = st.selectbox(
                        "Select City",
                        options=["Select City"] + cities_for_selected_state,
                    )

                    if select_location_city != "Select City":
                        city_name = select_location_city
                        # encode city name to handle spaces
                        # encoded_city = urllib.parse.quote(city_name)

                        aqi, pm25 = get_aqi_city(city_name)
                        # st.write(aqi, pm25)
                else:
                    # if no state selected, disable city box
                    st.selectbox("Select City", options=["Select City"], disabled=True)
                    aqi, pm25 = None, None

            # st.divider()

            st.header("Asthma Information")
            asthma_severity = st.selectbox(
                "Asthma Severity Level",
                ["Select Asthma Severity", "Moderate", "Severe", "Life Threatening"],
            )
            st.divider()

            get_recommendation = None
            # st.write("⬇️Click Me⬇️")

            # prevent user to select button
            if (
                select_location_state != "Select State"
                and select_location_city != "Select City"
                and asthma_severity != "Select Asthma Severity"
            ):
                col1, col2, col3 = st.columns([0.1, 1, 0.1])
                # centering button
                with col2:
                    get_recommendation = st.button(
                        "Get Recommendation", type="primary", use_container_width=True
                    )

            #  button in the sidebar
            # get_recommendation = st.button("Get Recommendations", type="primary")

        # check if rec button is presed and if we have AQI data
        if get_recommendation and aqi is not None and pm25 is not None:
            # display belwo in placeholder main page
            with main_content_placeholder.container():
                st.header("The verdict?")

                # since thers a few factors, will rank
                if aqi <= 50:
                    aqi_category = "Good"
                elif aqi <= 100:
                    aqi_category = "Moderate"
                elif aqi <= 150:
                    aqi_category = "Unhealthy for Sensitive Groups"
                elif aqi <= 200:
                    aqi_category = "Unhealthy"
                elif aqi <= 300:
                    aqi_category = "Very Unhealthy"
                else:
                    aqi_category = "Hazardous"

                # determine category based on PM2.5
                if pm25 <= 12:
                    pm25_category = "Good"
                elif pm25 <= 35.4:
                    pm25_category = "Moderate"
                elif pm25 <= 55.4:
                    pm25_category = "Unhealthy for Sensitive Groups"
                elif pm25 <= 150.4:
                    pm25_category = "Unhealthy"
                elif pm25 <= 250.4:
                    pm25_category = "Very Unhealthy"
                else:
                    pm25_category = "Hazardous"

                # compare which one is worser, pm2.5 or AQI
                category_ranking = [
                    "Good",
                    "Moderate",
                    "Unhealthy for Sensitive Groups",
                    "Unhealthy",
                    "Very Unhealthy",
                    "Hazardous",
                ]
                aqi_rank = category_ranking.index(aqi_category)
                pm25_rank = category_ranking.index(pm25_category)

                if pm25_rank > aqi_rank:
                    air_quality_category = pm25_category
                else:
                    air_quality_category = aqi_category

                # now check asthma severity
                recommendation = ""
                if air_quality_category == "Good":
                    if asthma_severity == "Moderate":
                        recommendation = (
                            "Safe for outdoor activities with normal precautions"
                        )
                    elif asthma_severity == "Severe":
                        recommendation = (
                            "Safe with extra precautions and medication on hand"
                        )
                    elif asthma_severity == "Life Threatening":
                        recommendation = (
                            "Limited outdoor activity recommended, keep sessions short"
                        )

                elif air_quality_category == "Moderate":
                    if asthma_severity == "Moderate":
                        recommendation = "Generally safe, but monitor symptoms"
                    elif asthma_severity == "Severe":
                        recommendation = "Caution advised, limit strenuous activities"
                    elif asthma_severity == "Life Threatening":
                        recommendation = "Indoor activities recommended"

                elif air_quality_category == "Unhealthy for Sensitive Groups":
                    if asthma_severity == "Moderate":
                        recommendation = (
                            "Safe with frequent breaks and monitoring symptoms"
                        )
                    else:
                        recommendation = "Outdoor activities not recommended"

                else:  # worst case scenario
                    recommendation = (
                        "Outdoor activities not recommended for children with asthma"
                    )

                # display assesmment
                if "not recommended" in recommendation:
                    st.error(recommendation)
                elif "Caution" in recommendation or "Limited" in recommendation:
                    st.warning(recommendation)
                else:
                    st.success(recommendation)

                # display gauge meter of aqi and pm2.5
                # st.write(aqi, pm25)

                col8, col9 = st.columns(2)
                with col8:

                    if aqi <= 50:
                        gauge_color = "green"
                    elif aqi <= 100:
                        gauge_color = "yellow"
                    elif aqi <= 150:
                        gauge_color = "orange"

                    fig = go.Figure(
                        go.Indicator(
                            mode="gauge+number",
                            value=aqi,
                            title={"text": "AQI"},
                            gauge={
                                "axis": {"range": [0, 100], "tickwidth": 1},
                                "bar": {"color": gauge_color},
                            },
                        )
                    )

                    # Display the figure in Streamlit
                    st.plotly_chart(fig, use_container_width=True)

                with col9:
                    if pm25 <= 12:
                        gauge_color = "green"
                    elif pm25 <= 35.5:
                        gauge_color = "yellow"
                    elif pm25 <= 55.4:
                        gauge_color = "orange"
                    elif pm25 <= 150.4:
                        gauge_color = "coral"

                    fig = go.Figure(
                        go.Indicator(
                            mode="gauge+number",
                            value=pm25,
                            title={"text": "PM2.5"},
                            gauge={
                                "axis": {"range": [0, 100], "tickwidth": 1},
                                "bar": {"color": gauge_color},
                            },
                        )
                    )

                    # plot gauuge chart
                    st.plotly_chart(fig, use_container_width=True)
                st.info("All data is in real-time")
                st.divider()
        elif get_recommendation:
            st.warning("Please select a state and city first to get a recommendation.")

        # this is the block to describe the inputs
        else:
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(
                    """
                    <div style="text-align: center;text-decoration: underline">
                        <h5>🏙️Why does your city matter?🏙️</h5>
                    </div>""",
                    unsafe_allow_html=True,
                )

                aqi_data = {
                    "AQI": [
                        "0 - 50",
                        "51 - 100",
                        "101 - 150",
                        "151 - 200",
                        "201 - 300",
                        "Above 300",
                    ],
                    "PM2.5": [
                        "0 - 12",
                        "12.1 - 35.4",
                        "35.5 - 55.4",
                        "55.5 - 150.4",
                        "150.5 - 250.4",
                        "Above 250.5",
                    ],
                    "Health Concern": [
                        "Good",
                        "Moderate",
                        "Unhealthy for sensitive groups",
                        "Unhealthy",
                        "Very unhealthy",
                        "Hazardous",
                    ],
                }

                aqi_df = pd.DataFrame(aqi_data)

                def highlight_health_concern(val):
                    color_map = {
                        "Good": "#7ABD7E",
                        "Moderate": "#F8D66D",
                        "Unhealthy for sensitive groups": "#FFB54C",
                        "Unhealthy": "#FF6961",
                        "Very unhealthy": "#CC93C2",
                        "Hazardous": "#ba1a0f",
                    }
                    return f"background-color: {color_map.get(val, 'white')}; color: white;"

                # apply style to health concern column
                styled_df = aqi_df.style.applymap(
                    highlight_health_concern, subset=["Health Concern"]
                )

                st.dataframe(styled_df, width=800, hide_index=True)

                st.info(
                    "**Urban areas tend to have poorer air quality due to industrial emissions, traffic pollution, and limited green spaces.**"
                )
                st.markdown(
                    """<p>Source: <a href='https://www.researchgate.net/publication/343404673/figure/tbl1/AS:920630392287232@1596506798348/Air-quality-index-AQI-values-PM25-and-PM10-conc-color-codes-air-pollutant-level-of.png' target='_blank' >Research Gate</a> </p>""",
                    unsafe_allow_html=True,
                )

            # information on asthma severity
            with col2:

                st.markdown(
                    """
                    <div style="text-align: center;text-decoration: underline">
                        <h5>😷How sever is your child's asthma?😷</h5>
                    </div>""",
                    unsafe_allow_html=True,
                )

                col3, col4 = st.columns([0.01, 5])
                # line divider vertvial
                with col3:
                    st.markdown(
                        """
                    <div class="divider-vertical-line"></div>
                        <style>
                        .divider-vertical-line {
                            border-left: 2px solid rgba(249, 180, 45, 1.0);
                            height: 400px;
                            margin: auto;""",
                        unsafe_allow_html=True,
                    )

                with col4:

                    asthma_sever_data = {
                        "😐Moderate Asthma 😐": [
                            "Able to talk",
                            "Heart rate ≤125/minute",
                            "Respiratory rate ≤30/minute",
                        ],
                        "❗Severe Asthma❗": [
                            "Too breathless to talk",
                            "Heart rate >125/minute",
                            "Respiratory rate >30/minute",
                        ],
                        "🚨Life-Threatening Asthma🚨": [
                            "Silent chest",
                            "Poor respiratory effort",
                            "Agitation",
                        ],
                    }

                    asthma_sever_df = pd.DataFrame(asthma_sever_data)

                    st.dataframe(asthma_sever_df, width=800, hide_index=True)

                    st.info(
                        "**Knowing a child's asthma severity helps prevent flare-ups outdoors. Those with severe asthma are more vulnerable to triggers like pollution and allergens, making precautions essential.**"
                    )
                    st.markdown(
                        """<p>Source: <a href='https://www.physio-pedia.com/images/0/0b/Screen_Shot_2017-01-25_at_12.53.38_AM.png' target='_blank' >Physiopedia</a> </p>""",
                        unsafe_allow_html=True,
                    )

    activity_risk_assessment_page()
except Exception as e:
    # show error
    st.error(f"An error occurred: {str(e)}")
