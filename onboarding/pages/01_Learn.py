import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import sqlite3
import os

# page config
st.set_page_config(
    page_title="Asthma & Air Quality: A Parent’s Guide",
    page_icon="🫁",
    layout="wide",
    initial_sidebar_state="auto",
)


# getting directory of database file
current_dir = os.path.dirname(os.path.abspath(__file__))

parent_dir = os.path.dirname(current_dir)
# connect to the database using the full path
conn = sqlite3.connect(os.path.join(parent_dir, "nafas.db"))


# fx to load data from database
def load_data_from_db():
    # load aqi data
    aqi_data = pd.read_sql_query("SELECT * FROM aqi_yearly_state", conn)

    # load asthma data
    asthma_data = pd.read_sql_query("SELECT * FROM prevalence_incidence_asthma", conn)

    return aqi_data, asthma_data


# load data from db file into dataframe
aqi_df, asthma_df = load_data_from_db()

# st.dataframe(aqi_df)
# st.dataframe(asthma_df)


# Title and introduction
st.markdown(
    """<h2>Understanding Asthma: Management & Trends</h2>""",
    unsafe_allow_html=True,
)
st.markdown(
    """<div style="text-align: justify;">This page provides parents with essential guidance on managing childhood asthma while also offering insights into air quality trends in Malaysia. Learn how to reduce asthma triggers and explore data on AQI and asthma prevalence in Malaysia to make informed decisions for your child’s health.</div>""",
    unsafe_allow_html=True,
)

tab1, tab2 = st.tabs(["🌟Understanding Asthma in Children🌟", "AQI & Asthma Trends"])


# Guide for parents
#############################################################################################

with tab1:
    st.header("Understanding asthma in your child 🧒👧🏽")
    st.subheader("And what to look out for!")

    st.markdown(
        """
    <img src="https://media0.giphy.com/media/v1.Y2lkPTc5MGI3NjExbjlpanpnbTVyYmN5MGptaWI2djN3cmZvd3lxNTlhZ25lMW93MDYybSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/ifIXLnBzbnQWdpyafa/giphy.gif" width="300">
    """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """<i>GIF Source: <a href='https://media0.giphy.com/media/v1.Y2lkPTc5MGI3NjExbjlpanpnbTVyYmN5MGptaWI2djN3cmZvd3lxNTlhZ25lMW93MDYybSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/ifIXLnBzbnQWdpyafa/giphy.gif' target='_self' >GIPHY</a></i>""",
        unsafe_allow_html=True,
    )

    st.markdown(
        "The below information is curated from the <a href='https://www.asthmafoundation.org.nz' target='_blank'>Asthma Respiratory Foundation NZ</a>.",
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
                """<p style='text-align: center;'>Download <a href='https://aafa.org/wp-content/uploads/2022/10/asthma-action-plan-aafa.pdf' target='_blank' >Here</a> </p>""",
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
                """<p style='text-align: center;'>Download <a href='https://www.physio-pedia.com/images/thumb/3/35/AsthmaDiary.png/444px-AsthmaDiary.png' target='_blank' >Here</a> </p>""",
                unsafe_allow_html=True,
            )


with tab2:

    # add image
    st.markdown(
        """<div style= "display: flex; justify-content: center"><img src="https://img.freepik.com/free-vector/diagram-showing-air-quality-index-with-color-scales_1308-40093.jpg?t=st=1741897924~exp=1741901524~hmac=547e53de934df60164787ec580e413590c0b8954d2d344af46c968988f8328ad&w=826" width="300"></div>""",
        unsafe_allow_html=True,
    )

    st.markdown(
        """<p style = "text-align : center;"><i>Image Source: <a href='https://img.freepik.com/free-vector/diagram-showing-air-quality-index-with-color-scales_1308-40093.jpg?t=st=1741897924~exp=1741901524~hmac=547e53de934df60164787ec580e413590c0b8954d2d344af46c968988f8328ad&w=826' target='_blank' >freepik</a></i></p>""",
        unsafe_allow_html=True,
    )
    st.markdown(
        """<h3>Overview of Trends</h3>""",
        unsafe_allow_html=True,
    )

    # for _ in range(1):
    #     st.write("")

    st.markdown(
        "<i>Air Quality Data is from <a href='https://www.kaggle.com/datasets/ynshung/malaysia-air-pollution-index' target='_blank'>Open Data Malaysia</a> via Kaggle while Asthma Dataset is from the  <a href='https://vizhub.healthdata.org/gbd-results/' target='_blank'>Institute for Health Metrics and Evaluation</a>.</i>",
        unsafe_allow_html=True,
    )

    @st.cache_data
    def get_aqi_data():
        return aqi_df

    @st.cache_data
    def get_ashtma_data():
        return asthma_df

    with st.expander("➡️ AQI by State & National Asthma Cases"):
        # handling error if databse cant be accessed
        try:
            aqi_data = get_aqi_data()
            asthma_data = get_ashtma_data()
        except Exception as e:
            st.error(f"Error loading data: {e}")
            st.info("Please ensure database can be accessed")
            aqi_data, asthma_data = None, None

        if aqi_data is not None and asthma_data is not None:

            # convert year to integer
            aqi_data["year"] = aqi_data["year"].astype(int)

            # list of unique states
            states = aqi_data["state"].unique().tolist()

            # default states to be shown to guide users
            default_states = (
                ["Kuala Lumpur", "Selangor"]
                if all(state in states for state in ["Kuala Lumpur", "Selangor"])
                else states[:2]
            )

            # allow multiple states to be selected
            selected_states = st.multiselect(
                "Select states to display👇",
                options=states,
                default=default_states,
            )

            if selected_states:
                # filter aqi data according to user selection
                filtered_aqi_data = aqi_data[aqi_data["state"].isin(selected_states)]

                fig = go.Figure()

                # group asthma by year and sum male and female
                asthma_yearly = (
                    asthma_data.groupby("year")
                    .apply(
                        lambda x: pd.Series(
                            {
                                "total_asthma": x[x["sex_name"] == "Male"]["val"].sum()
                                + x[x["sex_name"] == "Female"]["val"].sum()
                            }
                        )
                    )
                    .reset_index()
                )

                # add bar chart for asthma dataset

                fig.add_trace(
                    go.Bar(
                        x=asthma_yearly["year"],
                        y=asthma_yearly["total_asthma"],
                        name="Yearly Asthma Cases (0-19)",
                        # reduce transparency of color bar for later overlaying
                        marker_color="rgba(180, 180, 180, 0.4)",
                        width=0.8,
                        yaxis="y2",
                    )
                )

                # add line chart for aqi data
                for state in selected_states:
                    state_data = filtered_aqi_data[filtered_aqi_data["state"] == state]
                    fig.add_trace(
                        go.Scatter(
                            x=state_data["year"],
                            y=state_data["aqi"],
                            mode="lines+markers",
                            name=f"{state} AQI",
                            line=dict(width=3),
                        )
                    )

                #
                fig.update_layout(
                    title="Air Quality Index (AQI) by State and Total Asthma Cases in Children in Malaysia (2005 - 2022)",
                    xaxis=dict(title="Year", tickmode="linear"),
                    yaxis=dict(title="AQI Value", side="left"),
                    yaxis2=dict(
                        title="Asthma Cases",
                        side="right",
                        overlaying="y",
                        showgrid=False,
                    ),
                    # legend orientation
                    legend=dict(
                        orientation="h",
                        yanchor="top",
                        y=-0.2,
                        xanchor="center",
                        x=0.5,
                    ),
                    margin=dict(
                        b=100
                    ),  # add bottom margin to avoid it look close togetherat bootom of plot
                )

                st.plotly_chart(fig, use_container_width=True)

            # if aqi_data is not None and asthma_data is not None:
            #     # convert year to integer
            #     aqi_data["year"] = aqi_data["year"].astype(int)

            #     # lsi tof unique states
            #     states = aqi_data["state"].unique().tolist()

            #     # default states to be shown to guide users
            #     default_states = (
            #         ["Kuala Lumpur", "Selangor"]
            #         if all(state in states for state in ["Kuala Lumpur", "Selangor"])
            #         else states[:2]
            #     )

            #     # allow multiple states to eb selected
            #     selected_states = st.multiselect(
            #         "Select states to display👇",
            #         options=states,
            #         default=default_states,
            #     )

            #     if selected_states:
            #         # filter data according to user selection
            #         filtered_data = aqi_data[aqi_data["state"].isin(selected_states)]

            #         # creating line chart
            #         fig = px.line(
            #             filtered_data,
            #             x="year",
            #             y="aqi",
            #             color="state",
            #             markers=True,
            #             title="Air Quality Index (AQI) Trends From 2005 - 2022",
            #             labels={"aqi": "AQI Value", "year": "Year", "state": "State"},
            #         )

            #         st.plotly_chart(fig, use_container_width=True)

            # insights

            st.markdown(
                """<p style = "text-align: justify;">Air quality has gone up and down over the years, with all states experiencing similar patterns, like when everyone's air quality worsened dramatically in 2019, during the <a href='https://en.wikipedia.org/wiki/2019_Southeast_Asian_haze' target='_blank'>2019 ASEAN Haze</a>. However, the data shows childhood asthma cases (gray bars) reached their highest levels around 2008-2011, despite AQI readings being in a relatively moderate range during that period. This suggests factors beyond air quality may have influenced asthma rates during those years. There was also a notable improvement period around 2017-2018, when both AQI readings and asthma cases were at their lowest.</p>""",
                unsafe_allow_html=True,
            )

            st.markdown(
                """
                <p style = "text-align: justify;">As of 2022, air quality has somewhat stabilized but remains worse than the healthier levels seen in 2017. Parents should expect this trend to worsen as industrialization continues across Malaysia, with more vehicles and factories contributing to pollution.</p>""",
                unsafe_allow_html=True,
            )
        else:
            st.warning("Please select at least one state to display data")
    with st.expander("➡️ Asthma Cases in Children in Malaysia by `(Gender)`"):
        if asthma_data is not None:
            # Convert year column to integer if it's not already
            asthma_data["year"] = asthma_data["year"].astype(int)

            # Group by gender
            gender_yearly = (
                asthma_data.groupby(["year", "sex_name"])["val"].mean().reset_index()
            )

            # Grouped bar chart
            fig_gender = px.bar(
                gender_yearly,
                x="year",
                y="val",
                color="sex_name",
                barmode="group",
                title="Asthma Cases by Gender and Year (2005 - 2021)",
                labels={"year": "Year", "val": "Cases", "sex_name": "Gender"},
                color_discrete_map={"Male": "#2D7087", "Female": "#CF8282"},
            )

            # Customize the layout
            fig_gender.update_layout(
                xaxis=dict(tickmode="linear"),
                legend_title="Gender",
                yaxis_title="# of cases",
                plot_bgcolor="rgba(0,0,0,0)",
                height=500,
            )

            # show plot
            st.plotly_chart(fig_gender, use_container_width=True)

            st.markdown(
                """
                <div style="text-align: justify;">This graph shows childhood asthma cases in Malaysia by gender from 2005-2021. <span style="color: #0EC9FF;">Male</span> children consistently have higher rates than <span style="color: #FF10F0;">females</span>. Both genders saw peak cases around 2009-2010, followed by a gradual decline.</div>
                """,
                unsafe_allow_html=True,
            )

            st.markdown(
                """
                <div style="text-align: justify;"><br>Interestingly enough, there is a <a href='https://allergyasthmanetwork.org/news/the-asthma-gender-gap/' target='_blank'>study</a> where it was observed that <span style="color: #0EC9FF;">males</span> under 18 are more likely to have asthma in comparison to <span style="color: #FF10F0;">female</span> children. Asthma mortality is also <a href='https://allergyasthmanetwork.org/news/the-asthma-gender-gap/' target='_blank'>more common</a> in this gender group. This is due to the fact that <span style="color: #0EC9FF;">males</span> under 10 have <a href='https://pmc.ncbi.nlm.nih.gov/articles/PMC8783601/#:~:text=There%20is%20a%20clear%20sex,)%20%5B1%2C%202%5D.' target='_blank'>smaller airways</a> compared to <span style="color: #FF10F0;">females</span>.</div>
                """,
                unsafe_allow_html=True,
            )

    with st.expander("➡️ Asthma Cases in Children in Malaysia by `(Age)`"):

        # since ps is about 6-17, will filter out below 5
        filtered_data = asthma_data[asthma_data["age_name"] != "<5 years"]

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
            yaxis_title="# of cases",
            plot_bgcolor="rgba(0,0,0,0)",
            height=500,
        )

        # show plot
        st.plotly_chart(fig_age, use_container_width=True)

        st.markdown(
            """
            <p style = "text-align:justify;">This graph shows childhood asthma prevalence in Malaysia by age group from 2005-2021. Children aged <span style = "color: #4ECDC4;">10-19 years</span> consistently show higher rates than the <span style = "color: #FFD166;">5-9 age</span> group. Both groups experienced peak prevalence around 2009-2010, followed by a gradual decline through 2021.</p>

            <p style = "text-align:justify;">It's worth noting that while the <span style = "color: #FFD166;">5-9 age</span> group shows lower prevalence, this may be partly due to the narrower age range (5 years) compared to the <span style = "color: #4ECDC4;">10-19 age</span>  group. Despite this difference in age span, the pattern of higher rates in older children remains significant.</p>


            """,
            unsafe_allow_html=True,
        )
    st.divider()
