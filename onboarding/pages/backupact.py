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


# # def display_general_info():
# #     """Display general information about air quality and asthma"""
# #     st.markdown("## Understanding Air Quality and Asthma")

# #     col1, col2 = st.columns(2)

# #     with col1:
# #         st.markdown("### Air Quality Index (AQI) Categories")
# #         aqi_data = {
# #             "Category": [
# #                 "Good",
# #                 "Moderate",
# #                 "Unhealthy for Sensitive Groups",
# #                 "Unhealthy",
# #                 "Very Unhealthy",
# #                 "Hazardous",
# #             ],
# #             "Range": ["0-50", "51-100", "101-150", "151-200", "201-300", "301+"],
# #             "Impact": [
# #                 "Minimal",
# #                 "Minor",
# #                 "Moderate",
# #                 "Significant",
# #                 "Severe",
# #                 "Extreme",
# #             ],
# #         }

# #         st.dataframe(pd.DataFrame(aqi_data), hide_index=True)

# #     with col2:
# #         st.markdown("### How Air Quality Affects Asthma")
# #         st.markdown(
# #             """
# #         Poor air quality can trigger asthma symptoms by:
# #         - Irritating airways
# #         - Causing inflammation
# #         - Triggering bronchospasm
# #         - Increasing mucus production

# #         Children are especially vulnerable because:
# #         - Their lungs are still developing
# #         - They breathe more air per pound of body weight
# #         - They often spend more time outdoors
# #         """
# #         )


# # This function would be called from your main app
# # Example:
# # activity_risk_assessment_page()


# import streamlit as st
# from streamlit_extras.autocomplete import autocomplete
# import requests


# # Function to get place suggestions as user types
# def get_place_suggestions(query):
#     if not query or len(query) < 3:
#         return []

#     try:
#         # Use OpenStreetMap Nominatim API for suggestions
#         url = (
#             f"https://nominatim.openstreetmap.org/search?q={query}&format=json&limit=5"
#         )
#         response = requests.get(url, headers={"User-Agent": "ActivityRiskApp"})
#         data = response.json()

#         # Extract place names from results
#         places = [f"{item.get('display_name')}" for item in data]
#         return places
#     except:
#         return []


# # Create the autocomplete search bar
# selected_place = autocomplete(
#     "Search for location:",
#     get_place_suggestions,
#     placeholder="Type to search for a location (e.g., Shah Alam)",
#     on_select=lambda result: result,
#     debounce_time=300,  # Wait 300ms after typing before making API request
# )

# # Process the selected place if user makes a selection
# if selected_place:
#     st.success(f"Selected: {selected_place}")

#     # Get coordinates for the selected place
#     try:
#         url = f"https://nominatim.openstreetmap.org/search?q={selected_place}&format=json&limit=1"
#         response = requests.get(url, headers={"User-Agent": "ActivityRiskApp"})
#         data = response.json()

#         if data:
#             lat = float(data[0]["lat"])
#             lon = float(data[0]["lon"])
#             st.session_state.latitude = lat
#             st.session_state.longitude = lon
#             st.session_state.location_name = selected_place
#             st.write(f"Coordinates: {lat}, {lon}")
#     except Exception as e:
#         st.error(f"Error getting coordinates: {e}")
from streamlit_searchbox import st_searchbox
import pandas as pd
import streamlit as st
import requests

# Create DataFrame with cities in KL and Selangor
cities_df = pd.DataFrame(
    {
        "city": [
            # Kuala Lumpur cities/areas
            "Kuala Lumpur City Center",
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
            # Selangor cities
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
        ]
    }
)


def search_dataframe(searchterm: str) -> list:
    # Search the DataFrame for the searchterm
    if not searchterm:
        return []

    # Case-insensitive search in the city column (changed from title)
    results = cities_df[cities_df["city"].str.contains(searchterm, case=False)][
        "city"
    ].tolist()
    return results


# Pass search function to the searchbox
selected_value = st_searchbox(
    search_dataframe,
    placeholder="Search cities in KL and Selangor... ",
    key="df_search",
)

st.write(f"Selected value: {selected_value}")

import requests
import urllib.parse  # Add this import for URL encoding

if selected_value:
    selected_city_row = cities_df[cities_df["city"] == selected_value]
    st.write("Details:")
    st.write(selected_city_row)

    # Get just the city name as a string, not the DataFrame row
    city_name = selected_value  # This is already the city name string from st_searchbox

    # URL encode the city name to handle spaces properly
    encoded_city = urllib.parse.quote(city_name)

    def get_location(city):
        geo_url = f"https://nominatim.openstreetmap.org/search?city={city}&country=Malaysia&format=json"
        response = requests.get(geo_url, headers={"User-Agent": "ActivityRiskApp"})
        data = response.json()
        return geo_url

    # Use the encoded city name in the function
    url = get_location(encoded_city)
    st.write(f"URL: {url}")
