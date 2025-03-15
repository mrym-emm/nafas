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

tab1, tab2, tab3 = st.tabs(
    ["AQI Trends", "Asthma Trends", "🌟Understanding Asthma in Children🌟"]
)


with tab1:
    st.header("Overview of Air Quality in Malaysia by State")

    # add free stock image
    st.markdown(
        '<img src="https://img.freepik.com/free-vector/diagram-showing-air-quality-index-with-color-scales_1308-40093.jpg?t=st=1741897924~exp=1741901524~hmac=547e53de934df60164787ec580e413590c0b8954d2d344af46c968988f8328ad&w=826" width="400">',
        unsafe_allow_html=True,
    )
    st.markdown(
        "Image Source: <a href='https://img.freepik.com/free-vector/diagram-showing-air-quality-index-with-color-scales_1308-40093.jpg?t=st=1741897924~exp=1741901524~hmac=547e53de934df60164787ec580e413590c0b8954d2d344af46c968988f8328ad&w=826' target='_self' >freepik.</a>",
        unsafe_allow_html=True,
    )

    for _ in range(1):
        st.write("")

    st.markdown(
        "The below data is retrieved from the following dataset <i>Air Pollution Index (API) in Malaysia </i><a href='https://www.kaggle.com/datasets/ynshung/malaysia-air-pollution-index' target='_self'>via Kaggle.</a>",
        unsafe_allow_html=True,
    )

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
            "Select states to display👇",
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

        st.markdown(
            """
            Air quality has gone up and down over the years, with all states experiencing similar patterns - like when everyone's air quality worsened dramatically in 2019, likely during the <a href='https://en.wikipedia.org/wiki/2019_Southeast_Asian_haze' target='_self'>2019 ASEAN Haze</a>. There was also a notable improvement period around 2017-2018. 
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            """
            As of 2022, air quality has somewhat stabilized but remains worse than the healthier levels seen in 2017. Parents should expect this trend to worsen as industrialization continues across Malaysia, with more vehicles and factories contributing to pollution. Please visit the `🌟Understanding Asthma in Children🌟` section of this page.
            """,
            unsafe_allow_html=True,
        )
    else:
        st.warning("Data not available.")

    st.divider()

# loading asthma dataset
##############################################################################################
with tab2:
    st.subheader("Asthma Cases in Children👇")

    st.markdown(
        "The below data is retireved from the  <a href='https://vizhub.healthdata.org/gbd-results/' target='_self'>Institute for Health Metrics and Evaluation</a>.",
        unsafe_allow_html=True,
    )

    # add expander
    with st.expander("➡️ Prevalence of Asthma in Children in Malaysia `(Gender)`"):
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

            st.markdown(
                """
                This graph shows childhood asthma cases in Malaysia by gender from 2005-2021. <span style="color: #0EC9FF;">Male</span> children consistently have higher rates than <span style="color: #FF10F0;">females</span>. Both genders saw peak cases around 2009-2010, followed by a gradual decline.
                """,
                unsafe_allow_html=True,
            )

            st.markdown(
                """
                Interestingly enough, there is a <a href='https://allergyasthmanetwork.org/news/the-asthma-gender-gap/' target='_blank' style="text-decoration: none">study</a> where it was observed that <span style="color: #0EC9FF;">males</span> under 18 are more likely to have asthma in comparison to <span style="color: #FF10F0;">female</span> children. Asthma mortality is also <a href='https://allergyasthmanetwork.org/news/the-asthma-gender-gap/' target='_blank' style="text-decoration: none">more common</a> in this gender group. This is due to the fact that <span style="color: #0EC9FF;">males</span> under 10 have <a href='https://pmc.ncbi.nlm.nih.gov/articles/PMC8783601/#:~:text=There%20is%20a%20clear%20sex,)%20%5B1%2C%202%5D.' target='_blank' style="text-decoration: none">smaller airways</a> compared to <span style="color: #FF10F0;">females</span>.
                """,
                unsafe_allow_html=True,
            )

        except Exception as e:
            st.error(f"Error loading data: {e}")
            st.info("Please ensure database can be accessed")

    with st.expander("➡️ Prevalence of Asthma in Children in Malaysia `(Age)`"):
        try:

            # since ps is about 6-17, will filter out below 5
            filtered_data = data_asthma[data_asthma["age_name"] != "<5 years"]

            # group by year
            age_yearly = (
                filtered_data.groupby(["year", "age_name"])["val"].mean().reset_index()
            )

            # bar chart accoring to age
            fig_age = px.bar(
                age_yearly,
                x="year",
                y="val",
                color="age_name",
                barmode="group",
                title="Asthma Prevalence by Age Group and Year (2005 - 2021)",
                labels={"year": "Year", "val": "Prevalence", "age_name": "Age Group"},
                color_discrete_sequence=px.colors.qualitative.Pastel,
            )

            # adding titles
            fig_age.update_layout(
                xaxis=dict(tickmode="linear"),
                legend_title="Age Group",
                yaxis_title="Prevalence Value",
                plot_bgcolor="rgba(0,0,0,0)",
                height=500,
            )

            # show plot
            st.plotly_chart(fig_age, use_container_width=True)

            st.markdown(
                """
                This graph shows childhood asthma prevalence in Malaysia by age group from 2005-2021. Children aged 10-19 years consistently show higher rates than the 5-9 age group. Both groups experienced peak prevalence around 2009-2010, followed by a gradual decline through 2021.
                
                It's worth noting that while the 5-9 age group shows lower prevalence, this may be partly due to the narrower age range `(5 years)` compared to the 10-19 group `(10 years)`. Despite this difference in age span, the pattern of higher rates in older children remains significant.
                
        
                """,
                unsafe_allow_html=True,
            )

        except Exception as e:
            st.error(f"Error loading data: {e}")
            st.info("Please ensure database can be accessed")

        st.divider()


# Guide for parents
#############################################################################################

with tab3:
    st.header("Understanding asthma in your child 🧒👧🏽")
    st.subheader("And what to look out for!")

    st.markdown(
        """
    <img src="https://media0.giphy.com/media/v1.Y2lkPTc5MGI3NjExbjlpanpnbTVyYmN5MGptaWI2djN3cmZvd3lxNTlhZ25lMW93MDYybSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/ifIXLnBzbnQWdpyafa/giphy.gif" width="300">
    """,
        unsafe_allow_html=True,
    )

    st.markdown(
        "GIF Source: <a href='https://media0.giphy.com/media/v1.Y2lkPTc5MGI3NjExbjlpanpnbTVyYmN5MGptaWI2djN3cmZvd3lxNTlhZ25lMW93MDYybSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/ifIXLnBzbnQWdpyafa/giphy.gif' target='_self' >GIPHY</a>",
        unsafe_allow_html=True,
    )

    st.markdown(
        "The below information is curated from the <a href='https://www.asthmafoundation.org.nz/assets/documents/Managing-your-childs-asthma.pdf' target='_self'>Asthma Respiratory + Foundation NZ</a>.",
        unsafe_allow_html=True,
    )

    with st.expander("➡️ How does it feel?"):

        st.markdown(
            """
            To get an idea of how asthma feels for your child, try breathing in and out through a straw 🥤. 
                <ul>
                <li>First do it normally</li>
                <li>Then pinch the straws end</li>
                <li>Keep trying to breathe in and out</li>
                </ul>
                You will start to feel short of breath and you may feel tightness in your chest.
                Imagine how tiring this would feel! """,
            unsafe_allow_html=True,
        )

        st.markdown(
            """
        <img src="https://media1.giphy.com/media/v1.Y2lkPTc5MGI3NjExZWhmNWRmMjlibHhuMTh1Nmt2cGE0dGlpOGlqMnNvanZoN3JhMmJyaiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/tsX1MfWWGQYLJjgnch/giphy.gif" width="300">
        """,
            unsafe_allow_html=True,
        )
        st.markdown(
            "GIF Source: <a href='https://media1.giphy.com/media/v1.Y2lkPTc5MGI3NjExZWhmNWRmMjlibHhuMTh1Nmt2cGE0dGlpOGlqMnNvanZoN3JhMmJyaiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/tsX1MfWWGQYLJjgnch/giphy.gif' target='_self' >GIPHY</a>",
            unsafe_allow_html=True,
        )

    with st.expander("➡️ Common Triggers"):
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

    with st.expander("➡️ Asthma Symptoms"):
        col1, col2 = st.columns(2)

        with col1:
            st.markdown(
                """

            <ul>
            <li>Coughing</li>
            <li>Breathlessness</li>
            <li>Wheezing</li>
            <li>Tight feeling in the chest</li>
            </ul>
            """,
                unsafe_allow_html=True,
            )

    with st.expander("➡️ How to manage"):
        col1, col2 = st.columns(2)

        with col1:
            st.markdown(
                """
            `Have an Action Plan`<br>
            An asthma action plan guides medication use based on symptom changes, from mild flare-ups to emergencies. Your doctor fills it out and updates it yearly or when medications change. Ensure you & your child understand it.

            
            """,
                unsafe_allow_html=True,
            )

        with col2:
            st.markdown(
                """
            <div style="display: flex; justify-content: center; align-items: center; height: 100%; min-height: 300px;">
            <img src="https://aafa.org/wp-content/uploads/2024/05/asthma-action-plan-aafa.png" width="300" style="max-width: 100%; height: auto;">
            </div>
            """,
                unsafe_allow_html=True,
            )
            st.markdown(
                """<p style='text-align: center;'>Source <a href='https://aafa.org/asthma/asthma-treatment/asthma-treatment-action-plan/' target='_self' >Asthma & Allergy Foundation of America</a> </p>""",
                unsafe_allow_html=True,
            )
        st.divider()
        col3, col4 = st.columns(2)

        with col3:
            st.markdown(
                """
            `Have a Symptom Diary`<br>
            The symptom diary helps track asthma patterns, identify triggers, and assess medication effectiveness. It’s especially useful after diagnosis, medication changes, or symptom shifts. Over time, your child can manage it independently.

            
            """,
                unsafe_allow_html=True,
            )

        with col4:
            st.markdown(
                """
            <div style="display: flex; justify-content: center; align-items: center; height: 100%; min-height: 300px;">
            <img src="https://www.physio-pedia.com/images/thumb/3/35/AsthmaDiary.png/444px-AsthmaDiary.png" width="300" style="max-width: 100%; height: auto;">
            </div>
            """,
                unsafe_allow_html=True,
            )
            st.markdown(
                """<p style='text-align: center;'>Source <a href='https://www.physio-pedia.com/images/thumb/3/35/AsthmaDiary.png/444px-AsthmaDiary.png' target='_self' >Physiopedia</a> </p>""",
                unsafe_allow_html=True,
            )
