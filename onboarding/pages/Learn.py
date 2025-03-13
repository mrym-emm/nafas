# import streamlit as st

# st.set_page_config(
#     page_title="Risk Assessment",
#     page_icon="📈",
#     layout="wide",
#     initial_sidebar_state="auto",
# )


# st.header("Children & Asthma in Malaysia 💨🫁")

# st.subheader("Open Me!")
# with st.expander("Death Cases in "):
#     st.markdown("hehe")

# st.subheader("Common Asthma Triggers in Malaysia")
# col1, col2 = st.columns(2)

# with col1:
#     st.markdown(
#         """
#     - Air pollution (haze, vehicle emissions)
#     - High humidity and mold
#     - Dust mites
#     - Cigarette smoke
#     """
#     )

# with col2:
#     st.markdown(
#         """
#     - Pet dander
#     - Seasonal changes
#     - Exercise in polluted conditions
#     - Strong odors/chemicals
#     """
#     )


import streamlit as st
import pandas as pd
import plotly.express as px

# page config
st.set_page_config(
    page_title="Air Quality & Asthma Insights Malaysia",
    page_icon="🫁",
    layout="wide",
    initial_sidebar_state="auto",
)

# connecting to google sheet api
sheet_url = "https://docs.google.com/spreadsheets/d/1c43XS6gjrZQdlMf7a32JsSZzdrLc7MitWCAA6NTXeBs/edit?usp=sharing"
csv_export_url = sheet_url.replace("/edit?usp=sharing", "/export?format=csv")


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
        data = load_data(csv_export_url)
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

    st.write("Asthma Cases in Children")

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
