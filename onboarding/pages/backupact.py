# import streamlit as st
# import pandas as pd
# import numpy as np
# import plotly.express as px
# import plotly.graph_objects as go
# from datetime import datetime, timedelta


# def activity_risk_assessment_page():
#     st.title("Activity Risk Assessment")
#     st.subheader("Is it safe for my child to participate in outdoor activities?")

#     # Sidebar for user inputs
#     with st.sidebar:
#         st.header("Child Information")

#         # Child's asthma severity
#         asthma_severity = st.radio(
#             "Asthma Severity Level", ["Mild", "Moderate", "Severe"], index=1
#         )

#         # Activity type
#         activity_type = st.selectbox(
#             "Type of Activity",
#             [
#                 "Light (walking, slow cycling)",
#                 "Moderate (jogging, playground)",
#                 "Intense (sports, running)",
#             ],
#         )

#         # Activity duration
#         duration = st.slider("Activity Duration (minutes)", 15, 120, 30, step=15)

#         # Location input
#         location = st.text_input("Location (City)", "Enter your city")

#         st.divider()

#         # Button to get recommendations
#         get_recommendation = st.button("Get Recommendations", type="primary")

#     # Main content area
#     if get_recommendation and location != "Enter your city":
#         # Here you would integrate with your air quality API
#         # For demonstration, we'll use simulated data

#         # Simulate getting AQI data
#         # In your actual app, replace this with your API call
#         aqi_value = simulate_aqi_data(location)

#         # Display current air quality
#         display_current_air_quality(aqi_value, location)

#         # Generate and display recommendations
#         display_recommendations(aqi_value, asthma_severity, activity_type, duration)

#         # Show activity alternatives
#         show_activity_alternatives(aqi_value, asthma_severity)
#     else:
#         st.info(
#             "Please enter your location and click 'Get Recommendations' to receive personalized activity guidance for your child."
#         )

#         # Show general information about air quality and asthma
#         display_general_info()


# def simulate_aqi_data(location):
#     """
#     Simulate AQI data for demonstration.
#     In the real app, replace with actual API data.
#     """
#     # For demo purposes, generate a random AQI value
#     # In real implementation, this would be from your air quality API
#     return np.random.randint(20, 180)


# def get_aqi_category(aqi_value):
#     """Return the AQI category based on the value"""
#     if aqi_value <= 50:
#         return "Good", "green"
#     elif aqi_value <= 100:
#         return "Moderate", "yellow"
#     elif aqi_value <= 150:
#         return "Unhealthy for Sensitive Groups", "orange"
#     elif aqi_value <= 200:
#         return "Unhealthy", "red"
#     elif aqi_value <= 300:
#         return "Very Unhealthy", "purple"
#     else:
#         return "Hazardous", "maroon"


# def display_current_air_quality(aqi_value, location):
#     """Display the current air quality information"""
#     category, color = get_aqi_category(aqi_value)

#     # Create columns for layout
#     col1, col2 = st.columns([1, 2])

#     with col1:
#         # Create a gauge chart for AQI
#         fig = go.Figure(
#             go.Indicator(
#                 mode="gauge+number",
#                 value=aqi_value,
#                 domain={"x": [0, 1], "y": [0, 1]},
#                 title={"text": "Air Quality Index"},
#                 gauge={
#                     "axis": {"range": [0, 300], "tickwidth": 1},
#                     "bar": {"color": color},
#                     "steps": [
#                         {"range": [0, 50], "color": "green"},
#                         {"range": [50, 100], "color": "yellow"},
#                         {"range": [100, 150], "color": "orange"},
#                         {"range": [150, 200], "color": "red"},
#                         {"range": [200, 300], "color": "purple"},
#                     ],
#                     "threshold": {
#                         "line": {"color": "red", "width": 4},
#                         "thickness": 0.75,
#                         "value": aqi_value,
#                     },
#                 },
#             )
#         )

#         fig.update_layout(height=300)
#         st.plotly_chart(fig, use_container_width=True)

#     with col2:
#         st.markdown(f"### Current Air Quality in {location}")
#         st.markdown(f"**AQI: {aqi_value}**")
#         st.markdown(f"**Category: {category}**")

#         # Display pollutant information (in real app, get from API)
#         st.markdown("### Main Pollutants")
#         pollutants = {
#             "PM2.5": np.random.randint(5, 40),
#             "PM10": np.random.randint(10, 60),
#             "Ozone": np.random.randint(20, 100),
#             "NO2": np.random.randint(10, 50),
#         }

#         # Display as a horizontal bar chart
#         pollutant_df = pd.DataFrame(
#             {"Pollutant": list(pollutants.keys()), "Value": list(pollutants.values())}
#         )

#         pollutant_chart = px.bar(
#             pollutant_df,
#             x="Value",
#             y="Pollutant",
#             orientation="h",
#             color="Value",
#             color_continuous_scale=["green", "yellow", "orange", "red"],
#         )
#         pollutant_chart.update_layout(height=200)
#         st.plotly_chart(pollutant_chart, use_container_width=True)


# def display_recommendations(aqi_value, asthma_severity, activity_type, duration):
#     """Generate and display recommendations based on inputs"""
#     category, color = get_aqi_category(aqi_value)

#     # Calculate risk level based on multiple factors
#     risk_level = calculate_risk_level(
#         aqi_value, asthma_severity, activity_type, duration
#     )

#     st.markdown("## Activity Recommendation")

#     # Display recommendation based on risk level
#     if risk_level == "Low":
#         st.success(f"### Low Risk ✅")
#         st.markdown(
#             "It is generally safe for your child to participate in the planned outdoor activity."
#         )
#         st.markdown("### Precautions:")
#         st.markdown("- Have rescue medication available")
#         st.markdown("- Watch for any symptoms during activity")
#         st.markdown("- Ensure proper warm-up before intense activity")

#     elif risk_level == "Medium":
#         st.warning(f"### Medium Risk ⚠️")
#         st.markdown(
#             "Your child can participate with caution and additional precautions."
#         )
#         st.markdown("### Recommended Precautions:")
#         st.markdown("- Reduce activity intensity or duration")
#         st.markdown("- Use rescue medication before activity as a preventative measure")
#         st.markdown("- Take more frequent breaks")
#         st.markdown("- Monitor closely for symptoms")

#     else:  # High risk
#         st.error(f"### High Risk ❌")
#         st.markdown(
#             "It is not recommended for your child to participate in the planned outdoor activity today."
#         )
#         st.markdown("### Why?")
#         st.markdown(f"- Current AQI of {aqi_value} is in the **{category}** range")
#         st.markdown(
#             f"- {asthma_severity} asthma increases sensitivity to poor air quality"
#         )
#         st.markdown(
#             f"- {activity_type} can increase respiratory rate and exposure to pollutants"
#         )

#     # Show anticipated exposure
#     st.markdown("### Estimated Pollutant Exposure")
#     exposure_chart = create_exposure_chart(aqi_value, duration, activity_type)
#     st.plotly_chart(exposure_chart, use_container_width=True)


# def calculate_risk_level(aqi_value, asthma_severity, activity_type, duration):
#     """Calculate risk level based on various factors"""
#     # Convert inputs to numerical risk factors

#     # AQI risk
#     if aqi_value <= 50:
#         aqi_risk = 1
#     elif aqi_value <= 100:
#         aqi_risk = 2
#     elif aqi_value <= 150:
#         aqi_risk = 3
#     else:
#         aqi_risk = 4

#     # Asthma severity risk
#     severity_risk = {"Mild": 1, "Moderate": 2, "Severe": 3}[asthma_severity]

#     # Activity type risk
#     activity_risk = {
#         "Light (walking, slow cycling)": 1,
#         "Moderate (jogging, playground)": 2,
#         "Intense (sports, running)": 3,
#     }[activity_type]

#     # Duration risk
#     if duration <= 30:
#         duration_risk = 1
#     elif duration <= 60:
#         duration_risk = 2
#     else:
#         duration_risk = 3

#     # Calculate total risk score
#     risk_score = (
#         aqi_risk * 1.5 + severity_risk * 1.25 + activity_risk + duration_risk * 0.75
#     )

#     # Determine risk level
#     if risk_score < 7:
#         return "Low"
#     elif risk_score < 11:
#         return "Medium"
#     else:
#         return "High"


# def create_exposure_chart(aqi_value, duration, activity_type):
#     """Create a chart showing estimated pollutant exposure over time"""
#     # Calculate breathing rate multiplier based on activity
#     breathing_multiplier = {
#         "Light (walking, slow cycling)": 1.5,
#         "Moderate (jogging, playground)": 2.5,
#         "Intense (sports, running)": 4,
#     }[activity_type]

#     # Create time series for duration of activity
#     time_points = list(range(0, duration + 1, 5))

#     # Calculate exposure (simplified model)
#     base_exposure = aqi_value / 50  # baseline exposure
#     exposure = [base_exposure * breathing_multiplier * (t / 15) for t in time_points]
#     exposure = [min(e, 10) for e in exposure]  # cap for visualization

#     # Create dataframe
#     df = pd.DataFrame({"Time (minutes)": time_points, "Relative Exposure": exposure})

#     # Create line chart
#     fig = px.line(
#         df,
#         x="Time (minutes)",
#         y="Relative Exposure",
#         title="Estimated Pollutant Exposure During Activity",
#     )

#     # Add safe threshold line
#     threshold = 3.0
#     fig.add_hline(
#         y=threshold,
#         line_dash="dash",
#         line_color="red",
#         annotation_text="Recommended Limit",
#         annotation_position="bottom right",
#     )

#     fig.update_layout(height=300)
#     return fig


# def show_activity_alternatives(aqi_value, asthma_severity):
#     """Show alternative activities based on air quality and asthma severity"""
#     st.markdown("## Alternative Activities")

#     if aqi_value > 100 or asthma_severity == "Severe":
#         st.markdown("### Recommended Indoor Alternatives:")

#         col1, col2 = st.columns(2)

#         with col1:
#             st.markdown("#### Physical Activities")
#             st.markdown("- Indoor swimming in well-ventilated pools")
#             st.markdown("- Indoor gym classes with proper ventilation")
#             st.markdown("- Home exercise routines")
#             st.markdown("- Dance or yoga")

#         with col2:
#             st.markdown("#### Other Activities")
#             st.markdown("- Museum visits")
#             st.markdown("- Library trips")
#             st.markdown("- Indoor crafts and projects")
#             st.markdown("- Board games and puzzles")
#     else:
#         st.markdown("### Alternative Outdoor Options:")
#         st.markdown("- Morning activities when pollution is typically lower")
#         st.markdown("- Activities in parks with more trees and away from traffic")
#         st.markdown("- Shorter duration activities with more breaks")
#         st.markdown("- Water-based activities that may reduce pollen exposure")


# def display_general_info():
#     """Display general information about air quality and asthma"""
#     st.markdown("## Understanding Air Quality and Asthma")

#     col1, col2 = st.columns(2)

#     with col1:
#         st.markdown("### Air Quality Index (AQI) Categories")
#         aqi_data = {
#             "Category": [
#                 "Good",
#                 "Moderate",
#                 "Unhealthy for Sensitive Groups",
#                 "Unhealthy",
#                 "Very Unhealthy",
#                 "Hazardous",
#             ],
#             "Range": ["0-50", "51-100", "101-150", "151-200", "201-300", "301+"],
#             "Impact": [
#                 "Minimal",
#                 "Minor",
#                 "Moderate",
#                 "Significant",
#                 "Severe",
#                 "Extreme",
#             ],
#         }

#         st.dataframe(pd.DataFrame(aqi_data), hide_index=True)

#     with col2:
#         st.markdown("### How Air Quality Affects Asthma")
#         st.markdown(
#             """
#         Poor air quality can trigger asthma symptoms by:
#         - Irritating airways
#         - Causing inflammation
#         - Triggering bronchospasm
#         - Increasing mucus production

#         Children are especially vulnerable because:
#         - Their lungs are still developing
#         - They breathe more air per pound of body weight
#         - They often spend more time outdoors
#         """
#         )


# # This function would be called from your main app
# # Example:
# activity_risk_assessment_page()


# # import streamlit as st
# # import pandas as pd
# # import numpy as np
# # import plotly.express as px
# # import plotly.graph_objects as go
# # from datetime import datetime, timedelta


# # def activity_risk_assessment_page():
# #     st.title("Activity Risk Assessment")
# #     st.subheader("Is it safe for my child to participate in outdoor activities?")

# #     # Sidebar for user inputs
# #     with st.sidebar:
# #         st.header("Child Information")

# #         # Child's asthma severity
# #         asthma_severity = st.radio(
# #             "Asthma Severity Level", ["Mild", "Moderate", "Severe"], index=1
# #         )

# #         # Activity type
# #         activity_type = st.selectbox(
# #             "Type of Activity",
# #             [
# #                 "Light (walking, slow cycling)",
# #                 "Moderate (jogging, playground)",
# #                 "Intense (sports, running)",
# #             ],
# #         )

# #         # Activity duration
# #         duration = st.slider("Activity Duration (minutes)", 15, 120, 30, step=15)

# #         # Location selection from your 5 available locations
# #         location = st.selectbox(
# #             "Location",
# #             [
# #                 "Bukit Jalil, KL",
# #                 "Cheras, KL",
# #                 "Putrajaya",
# #                 "Batu Muda, KL",
# #                 "Shah Alam, Selangor",
# #                 "Kuala Selangor, Selangor",
# #                 "Petaling Jaya, Selangor",
# #                 "Banting, Selangor",
# #             ],
# #             index=0,
# #         )

# #         st.divider()

# #         # Button to get recommendations
# #         get_recommendation = st.button("Get Recommendations", type="primary")


# #     # Main content area
# #     if get_recommendation:
# #         # Here you would integrate with your air quality API
# #         # For demonstration, we'll use simulated data

# #         # Simulate getting AQI data
# #         # In your actual app, replace this with your API call
# #         aqi_value = simulate_aqi_data(location)

# #         # Display current air quality
# #         display_current_air_quality(aqi_value, location)

# #         # Generate and display recommendations
# #         display_recommendations(aqi_value, asthma_severity, activity_type, duration)

# #         # Show activity alternatives
# #         show_activity_alternatives(aqi_value, asthma_severity)
# #     else:
# #         st.info(
# #             "Please enter your location and click 'Get Recommendations' to receive personalized activity guidance for your child."
# #         )

# #         # Show general information about air quality and asthma
# #         display_general_info()


# # def get_real_time_aqi_data(location):
# #     """
# #     Get real-time AQI data for the selected location.
# #     This function should connect to your existing air quality data source.
# #     """
# #     # Integrate with your existing real-time air quality data
# #     # Replace this with your actual implementation to fetch real data

# #     # If you already have a function that gets AQI data in your dashboard,
# #     # you can call that function here

# #     try:
# #         # Example of how you might retrieve the data from your existing system
# #         # aqi_value = your_existing_function_to_get_aqi(location)

# #         # Placeholder until integrated with your actual data source
# #         aqi_value = get_mock_aqi_for_location(location)
# #         return aqi_value
# #     except Exception as e:
# #         st.error(f"Error retrieving air quality data: {e}")
# #         return 50  # Return a default moderate value as fallback


# # def get_mock_aqi_for_location(location):
# #     """
# #     This is a temporary function to return different AQI values based on location.
# #     Replace this with your actual data retrieval once integrated.
# #     """
# #     # This mimics what real data might look like with different values per city
# #     mock_data = {
# #         "New York": 65,
# #         "Los Angeles": 88,
# #         "Chicago": 42,
# #         "Houston": 76,
# #         "Phoenix": 103,
# #     }
# #     return mock_data.get(location, 50)


# # def get_aqi_category(aqi_value):
# #     """Return the AQI category based on the value"""
# #     if aqi_value <= 50:
# #         return "Good", "green"
# #     elif aqi_value <= 100:
# #         return "Moderate", "yellow"
# #     elif aqi_value <= 150:
# #         return "Unhealthy for Sensitive Groups", "orange"
# #     elif aqi_value <= 200:
# #         return "Unhealthy", "red"
# #     elif aqi_value <= 300:
# #         return "Very Unhealthy", "purple"
# #     else:
# #         return "Hazardous", "maroon"


# # def display_current_air_quality(aqi_value, location):
# #     """Display the current air quality information"""
# #     category, color = get_aqi_category(aqi_value)

# #     # Create columns for layout
# #     col1, col2 = st.columns([1, 2])

# #     with col1:
# #         # Create a gauge chart for AQI
# #         fig = go.Figure(
# #             go.Indicator(
# #                 mode="gauge+number",
# #                 value=aqi_value,
# #                 domain={"x": [0, 1], "y": [0, 1]},
# #                 title={"text": "Air Quality Index"},
# #                 gauge={
# #                     "axis": {"range": [0, 300], "tickwidth": 1},
# #                     "bar": {"color": color},
# #                     "steps": [
# #                         {"range": [0, 50], "color": "green"},
# #                         {"range": [50, 100], "color": "yellow"},
# #                         {"range": [100, 150], "color": "orange"},
# #                         {"range": [150, 200], "color": "red"},
# #                         {"range": [200, 300], "color": "purple"},
# #                     ],
# #                     "threshold": {
# #                         "line": {"color": "red", "width": 4},
# #                         "thickness": 0.75,
# #                         "value": aqi_value,
# #                     },
# #                 },
# #             )
# #         )

# #         fig.update_layout(height=300)
# #         st.plotly_chart(fig, use_container_width=True)

# #     with col2:
# #         st.markdown(f"### Current Air Quality in {location}")
# #         st.markdown(f"**AQI: {aqi_value}**")
# #         st.markdown(f"**Category: {category}**")

# #         # Display pollutant information (in real app, get from API)
# #         st.markdown("### Main Pollutants")
# #         pollutants = {
# #             "PM2.5": np.random.randint(5, 40),
# #             "PM10": np.random.randint(10, 60),
# #             "Ozone": np.random.randint(20, 100),
# #             "NO2": np.random.randint(10, 50),
# #         }

# #         # Display as a horizontal bar chart
# #         pollutant_df = pd.DataFrame(
# #             {"Pollutant": list(pollutants.keys()), "Value": list(pollutants.values())}
# #         )

# #         pollutant_chart = px.bar(
# #             pollutant_df,
# #             x="Value",
# #             y="Pollutant",
# #             orientation="h",
# #             color="Value",
# #             color_continuous_scale=["green", "yellow", "orange", "red"],
# #         )
# #         pollutant_chart.update_layout(height=200)
# #         st.plotly_chart(pollutant_chart, use_container_width=True)


# # def display_recommendations(aqi_value, asthma_severity, activity_type, duration):
# #     """Generate and display recommendations based on inputs"""
# #     category, color = get_aqi_category(aqi_value)

# #     # Calculate risk level based on multiple factors
# #     risk_level = calculate_risk_level(
# #         aqi_value, asthma_severity, activity_type, duration
# #     )

# #     st.markdown("## Activity Recommendation")

# #     # Display recommendation based on risk level
# #     if risk_level == "Low":
# #         st.success(f"### Low Risk ✅")
# #         st.markdown(
# #             "It is generally safe for your child to participate in the planned outdoor activity."
# #         )
# #         st.markdown("### Precautions:")
# #         st.markdown("- Have rescue medication available")
# #         st.markdown("- Watch for any symptoms during activity")
# #         st.markdown("- Ensure proper warm-up before intense activity")

# #     elif risk_level == "Medium":
# #         st.warning(f"### Medium Risk ⚠️")
# #         st.markdown(
# #             "Your child can participate with caution and additional precautions."
# #         )
# #         st.markdown("### Recommended Precautions:")
# #         st.markdown("- Reduce activity intensity or duration")
# #         st.markdown("- Use rescue medication before activity as a preventative measure")
# #         st.markdown("- Take more frequent breaks")
# #         st.markdown("- Monitor closely for symptoms")

# #     else:  # High risk
# #         st.error(f"### High Risk ❌")
# #         st.markdown(
# #             "It is not recommended for your child to participate in the planned outdoor activity today."
# #         )
# #         st.markdown("### Why?")
# #         st.markdown(f"- Current AQI of {aqi_value} is in the **{category}** range")
# #         st.markdown(
# #             f"- {asthma_severity} asthma increases sensitivity to poor air quality"
# #         )
# #         st.markdown(
# #             f"- {activity_type} can increase respiratory rate and exposure to pollutants"
# #         )

# #     # Show anticipated exposure
# #     st.markdown("### Estimated Pollutant Exposure")
# #     exposure_chart = create_exposure_chart(aqi_value, duration, activity_type)
# #     st.plotly_chart(exposure_chart, use_container_width=True)


# # def calculate_risk_level(aqi_value, asthma_severity, activity_type, duration):
# #     """Calculate risk level based on various factors"""
# #     # Convert inputs to numerical risk factors

# #     # AQI risk
# #     if aqi_value <= 50:
# #         aqi_risk = 1
# #     elif aqi_value <= 100:
# #         aqi_risk = 2
# #     elif aqi_value <= 150:
# #         aqi_risk = 3
# #     else:
# #         aqi_risk = 4

# #     # Asthma severity risk
# #     severity_risk = {"Mild": 1, "Moderate": 2, "Severe": 3}[asthma_severity]

# #     # Activity type risk
# #     activity_risk = {
# #         "Light (walking, slow cycling)": 1,
# #         "Moderate (jogging, playground)": 2,
# #         "Intense (sports, running)": 3,
# #     }[activity_type]

# #     # Duration risk
# #     if duration <= 30:
# #         duration_risk = 1
# #     elif duration <= 60:
# #         duration_risk = 2
# #     else:
# #         duration_risk = 3

# #     # Calculate total risk score
# #     risk_score = (
# #         aqi_risk * 1.5 + severity_risk * 1.25 + activity_risk + duration_risk * 0.75
# #     )

# #     # Determine risk level
# #     if risk_score < 7:
# #         return "Low"
# #     elif risk_score < 11:
# #         return "Medium"
# #     else:
# #         return "High"


# # def create_exposure_chart(aqi_value, duration, activity_type):
# #     """Create a chart showing estimated pollutant exposure over time"""
# #     # Calculate breathing rate multiplier based on activity
# #     breathing_multiplier = {
# #         "Light (walking, slow cycling)": 1.5,
# #         "Moderate (jogging, playground)": 2.5,
# #         "Intense (sports, running)": 4,
# #     }[activity_type]

# #     # Create time series for duration of activity
# #     time_points = list(range(0, duration + 1, 5))

# #     # Calculate exposure (simplified model)
# #     base_exposure = aqi_value / 50  # baseline exposure
# #     exposure = [base_exposure * breathing_multiplier * (t / 15) for t in time_points]
# #     exposure = [min(e, 10) for e in exposure]  # cap for visualization

# #     # Create dataframe
# #     df = pd.DataFrame({"Time (minutes)": time_points, "Relative Exposure": exposure})

# #     # Create line chart
# #     fig = px.line(
# #         df,
# #         x="Time (minutes)",
# #         y="Relative Exposure",
# #         title="Estimated Pollutant Exposure During Activity",
# #     )

# #     # Add safe threshold line
# #     threshold = 3.0
# #     fig.add_hline(
# #         y=threshold,
# #         line_dash="dash",
# #         line_color="red",
# #         annotation_text="Recommended Limit",
# #         annotation_position="bottom right",
# #     )

# #     fig.update_layout(height=300)
# #     return fig


# # def show_activity_alternatives(aqi_value, asthma_severity):
# #     """Show alternative activities based on air quality and asthma severity"""
# #     st.markdown("## Alternative Activities")

# #     if aqi_value > 100 or asthma_severity == "Severe":
# #         st.markdown("### Recommended Indoor Alternatives:")

# #         col1, col2 = st.columns(2)

# #         with col1:
# #             st.markdown("#### Physical Activities")
# #             st.markdown("- Indoor swimming in well-ventilated pools")
# #             st.markdown("- Indoor gym classes with proper ventilation")
# #             st.markdown("- Home exercise routines")
# #             st.markdown("- Dance or yoga")

# #         with col2:
# #             st.markdown("#### Other Activities")
# #             st.markdown("- Museum visits")
# #             st.markdown("- Library trips")
# #             st.markdown("- Indoor crafts and projects")
# #             st.markdown("- Board games and puzzles")
# #     else:
# #         st.markdown("### Alternative Outdoor Options:")
# #         st.markdown("- Morning activities when pollution is typically lower")
# #         st.markdown("- Activities in parks with more trees and away from traffic")
# #         st.markdown("- Shorter duration activities with more breaks")
# #         st.markdown("- Water-based activities that may reduce pollen exposure")


from streamlit_searchbox import st_searchbox
import pandas as pd
import streamlit as st
import requests

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
                    "Seri Kembangan",
                    "Damansara",
                    "Gombak",
                    "Port Klang",
                    "Sungai Buloh",
                    "Hulu Langat",
                    "Kuala Selangor",
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
            placeholder="Kuala Lumpur",
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
        st.title("Is it safe for my child to participate in outdoor activities?")
        st.subheader("Find out now by taking our assessment check on the sidebar!")

        st.divider()

        # Create a placeholder in the main area for content that will appear after button click
        main_content_placeholder = st.empty()

        with st.sidebar:
            st.header("⬇️Fill in the below⬇️")
            st.subheader("Type in your city")
            aqi, pm25 = get_user_current_info()

            st.divider()

            st.header("Asthma Information")
            asthma_severity = st.radio(
                "Asthma Severity Level",
                ["Moderate", "Severe", "Life Threatening"],
                index=1,
            )
            st.divider()

            # Create the button in the sidebar
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
                st.write(aqi, pm25)

        # this is the block to describe the inputs
        else:
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(
                    """
                    <div style="text-align: center;text-decoration: underline">
                        <h3>🏙️Why does your city matter?🏙️</h3>
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
                        <h3>😷How sever is your child's asthma?😷</h3>
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
