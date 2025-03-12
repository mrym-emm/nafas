import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta


st.set_page_config(
    page_title="Risk Assessment",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="auto",
)


def activity_risk_assessment_page():
    st.title("Activity Risk Assessment")
    st.subheader("Is it safe for my child to participate in outdoor activities?")
    st.subheader("⬅️Find out now!")

    # Sidebar for user inputs
    with st.sidebar:
        st.header("Child Information")

        # Child's asthma severity
        asthma_severity = st.radio(
            "Asthma Severity Level", ["Mild", "Moderate", "Severe"], index=1
        )

        # Activity type
        activity_type = st.selectbox(
            "Type of Activity",
            [
                "Light (walking, slow cycling)",
                "Moderate (jogging, playground)",
                "Intense (sports, running)",
            ],
        )

        # Activity duration
        duration = st.slider("Activity Duration (minutes)", 15, 120, 30, step=15)

        # Location selection from your 5 available locations
        location = st.selectbox(
            "Location",
            [
                "Select",
                "Bukit Jalil, KL",
                "Cheras, KL",
                "Putrajaya",
                "Batu Muda, KL",
                "Shah Alam, Selangor",
                "Kuala Selangor, Selangor",
                "Petaling Jaya, Selangor",
                "Banting, Selangor",
            ],
            index=0,
        )

        st.divider()

        # Button to get recommendations
        get_recommendation = st.button("Get Recommendations", type="primary")

    st.divider()
    if get_recommendation and location != "Select":
        st.header("Main content")
        if location == "Shah Alam, Selangor":
            st.write("Yes")


activity_risk_assessment_page()
