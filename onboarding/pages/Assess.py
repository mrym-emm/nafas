from streamlit_searchbox import st_searchbox
import pandas as pd
import streamlit as st
import requests
import plotly.graph_objects as go

import urllib.parse  # for url encodiing

st.set_page_config(
    page_title="Risk Assessment",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="auto",
)

try:
    # getting current user aqi, pm2.5
    def get_user_current_info():
        # citites df
        cities_df = pd.DataFrame(
            {
                "city": [
                    # kl
                    "Kuala Lumpur",
                    "Bukit Bintang",
                    "Chow Kit",
                    "Kampung Baru",
                    "Bangsar",
                    "Mont Kiara",
                    "Brickfields",
                    "Sentul",
                    "Wangsa Maju",
                    "Setapak",
                    "Kepong",
                    "Segambut",
                    "Cheras",
                    "Sri Petaling",
                    "Desa Petaling",
                    # slgr
                    "Shah Alam",
                    "Petaling Jaya",
                    "Subang Jaya",
                    "Klang",
                    "Ampang",
                    "Kajang",
                    "Bangi",
                    "Puchong",
                    "Rawang",
                    "Semenyih",
                    "Cyberjaya",
                    "Putrajaya",
                    "Sepang",
                    "Damansara",
                    "Gombak",
                    "Port Klang",
                    "Sungai Buloh",
                    "Hulu Langat",
                    "Kemaman",
                ]
            }
        )

        def search_dataframe(searchterm: str) -> list:
            # search the city df
            if not searchterm:
                return []

            # allwoing case insensitibve
            results = cities_df[cities_df["city"].str.contains(searchterm, case=False)][
                "city"
            ].tolist()
            return results

        # pass search function to the searchbox
        selected_value = st_searchbox(
            search_dataframe,
            placeholder="Insert city...",
            key="df_search",
        )

        if selected_value:
            # selected_city_row = cities_df[cities_df["city"] == selected_value]

            # reassinging the selcted value to the city name
            city_name = selected_value

            # encode city name to handle spaces
            encoded_city = urllib.parse.quote(city_name)

            def get_aqi_city(city):
                geo_url = f"https://nominatim.openstreetmap.org/search?city={city}&country=Malaysia&format=json"
                response = requests.get(
                    geo_url, headers={"User-Agent": "ActivityRiskApp"}
                )
                data = response.json()
                lat, long = data[0].get("lat"), data[0].get("lon")

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

            # getting the values
            aqi, pm25 = get_aqi_city(encoded_city)

            return aqi, pm25

    def activity_risk_assessment_page():
        st.title("Should my child go outside?")
        st.subheader("Find out now by taking our assessment check in the sidebar!")

        st.divider()

        # create a placeholder in the main area for content that will show after rec button iz click
        main_content_placeholder = st.empty()

        with st.sidebar:
            st.header("⬇️Fill in the below⬇️")
            st.subheader("Type in your city")
            aqi, pm25 = get_user_current_info()

            # st.divider()

            st.header("Asthma Information")
            asthma_severity = st.selectbox(
                "Asthma Severity Level",
                ["Moderate", "Severe", "Life Threatening"],
                index=1,
            )
            st.divider()

            st.write("⬇️Click Me⬇️")

            #  button in the sidebar
            get_recommendation = st.button("Get Recommendations", type="primary")

        # cehck if rec button is presed
        if get_recommendation:
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

                    # Display the figure in Streamlit
                    st.plotly_chart(fig, use_container_width=True)
                st.divider()

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
except:
    print("")
