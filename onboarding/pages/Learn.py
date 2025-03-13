import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# page config
st.set_page_config(
    page_title="Air Quality & Asthma Insights Malaysia",
    page_icon="🫁",
    layout="wide",
    initial_sidebar_state="auto",
)

# connecting to google sheet api for aqi state
aqi_sheet_url = "https://docs.google.com/spreadsheets/d/1c43XS6gjrZQdlMf7a32JsSZzdrLc7MitWCAA6NTXeBs/edit?usp=sharing"
csv_export_url_aqi = aqi_sheet_url.replace("/edit?usp=sharing", "/export?format=csv")

# connecting to google sheet api for asthma
asthma_sheet_url = "https://docs.google.com/spreadsheets/d/1MFEz402SYOU21KqPmVFfJggmiNFSat4VcCr7vG-kflQ/edit?usp=sharing"
csv_export_url_asthma = asthma_sheet_url.replace(
    "/edit?usp=sharing", "/export?format=csv"
)


# Title and introduction
st.title("Insights on Air Quality and Asthma in Malaysia")
st.markdown(
    """
This page provides data insights about the relationship between air quality
and asthma in Malaysia to help parents better understand and manage asthma triggers.
"""
)

tab1, tab2 = st.tabs(["AQI & Asthma Trends", "Understanding Asthma in Children"])


with tab1:
    st.header("Overview of Air Quality and Asthma in Malaysia")

    # read data directly using pandas

    # caches the data to improve performance
    @st.cache_data
    def load_data(url):
        return pd.read_csv(url)

    try:
        data = load_data(csv_export_url_aqi)
        # st.dataframe(data)
    except Exception as e:
        st.error(f"Error loading data: {e}")
        st.info("Please ensure database can be accessed")

    if data is not None:
        # ensure the Year column is treated as an integer
        data["Year"] = data["Year"].astype(int)

        # user can select state
        selected_states = st.multiselect(
            "Select states to display",
            options=data.columns[1:],
            default=["Kuala Lumpur", "Selangor"],
        )

        # converting wide to long format using melt
        df_melted = data.melt(
            id_vars=["Year"],
            value_vars=selected_states,
            var_name="State",
            value_name="AQI",
        )

        # kreate hte line chart
        fig = px.line(
            df_melted,
            x="Year",
            y="AQI",
            color="State",
            markers=True,
            title="Air Quality Index (AQI) Trends From 2005 - 2022",
            labels={"AQI": "AQI Value", "Year": "Year", "State": "State"},
        )

        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Data not available.")

    st.divider()

    # loading asthma dataset
    ##############################################################################################
    st.subheader("Asthma Cases in Children👇")

    st.markdown(
        "The below data is retireved from the  <a href='https://vizhub.healthdata.org/gbd-results/' target='_self'>Institute for Health Metrics and Evaluation</a>",
        unsafe_allow_html=True,
    )

    # add expander
with st.expander("Prevalence of Asthma in Children in Malaysia (Gender)"):
    try:
        data_asthma = load_data(csv_export_url_asthma)
        # st.dataframe(data_asthma)

        # group by gender
        gender_yearly = (
            data_asthma.groupby(["year", "sex_name"])["val"].mean().reset_index()
        )

        # grouped bar chart
        fig_gender = px.bar(
            gender_yearly,
            x="year",
            y="val",
            color="sex_name",
            barmode="group",
            title="Asthma Prevalence by Gender and Year (2005 - 2021)",
            labels={"year": "Year", "val": "Prevalence", "sex_name": "Gender"},
            color_discrete_map={"Male": "#2D7087", "Female": "#CF8282"},
        )

        # Customize the layout
        fig_gender.update_layout(
            xaxis=dict(tickmode="linear"),
            legend_title="Gender",
            yaxis_title="Prevalence Value",
            plot_bgcolor="rgba(0,0,0,0)",
            height=500,
        )

        # show plot
        st.plotly_chart(fig_gender, use_container_width=True)

    except Exception as e:
        st.error(f"Error loading data: {e}")
        st.info("Please ensure database can be accessed")

with st.expander("Prevalence of Asthma in Children in Malaysia (Age)"):
    try:

        # Filter out the "under 5" age group
        filtered_data = data_asthma[data_asthma["age_name"] != "<5 years"]

        # Group by year and age instead of gender
        age_yearly = (
            filtered_data.groupby(["year", "age_name"])["val"].mean().reset_index()
        )

        # Create bar chart by age groups
        fig_age = px.bar(
            age_yearly,
            x="year",
            y="val",
            color="age_name",
            barmode="group",
            title="Asthma Prevalence by Age Group and Year (2005 - 2021)",
            labels={"year": "Year", "val": "Prevalence", "age_name": "Age Group"},
            color_discrete_sequence=px.colors.qualitative.Pastel,  # You can choose different color schemes
        )

        # Customize the layout
        fig_age.update_layout(
            xaxis=dict(tickmode="linear"),
            legend_title="Age Group",
            yaxis_title="Prevalence Value",
            plot_bgcolor="rgba(0,0,0,0)",
            height=500,
        )

        # Show plot
        st.plotly_chart(fig_age, use_container_width=True)

    except Exception as e:
        st.error(f"Error loading data: {e}")
        st.info("Please ensure database can be accessed")


# Guide for parents
#############################################################################################
with tab2:
    st.header("Understanding how the air affects your child 🧒")
    st.subheader("And what to look out for!")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
            """
        - Air pollution (haze, vehicle emissions)
        - High humidity and mold
        - Dust mites
        - Cigarette smoke
        """
        )

    with col2:
        st.markdown(
            """
        - Pet dander
        - Seasonal changes
        - Exercise in polluted conditions
        - Strong odors/chemicals
        """
        )
