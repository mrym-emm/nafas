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

# import streamlit as st
# import pandas as pd
# import matplotlib.pyplot as plt
# import seaborn as sns
# import plotly.express as px
# import plotly.graph_objects as go
# from plotly.subplots import make_subplots

# # Page configuration
# st.set_page_config(
#     page_title="Air Quality & Asthma Insights Malaysia", page_icon="🫁", layout="wide"
# )

# # Title and introduction
# st.title("Insights on Air Quality and Asthma in Malaysia")
# st.markdown(
#     """
# This dashboard provides data insights about the relationship between air quality
# and asthma in Malaysia to help parents better understand and manage asthma triggers.
# """
# )

# tab1, tab2, tab3, tab4 = st.tabs(
#     ["Overview", "AQI Trends", "Asthma Statistics", "Correlation Analysis"]
# )


# with tab1:
#     st.header("Overview of Air Quality and Asthma in Malaysia")


import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import gspread
from google.oauth2 import service_account
from streamlit_gsheets import GSheetsConnection


# Page configuration
st.set_page_config(
    page_title="Air Quality & Asthma Insights Malaysia", page_icon="🫁", layout="wide"
)


url = "https://docs.google.com/spreadsheets/d/1c43XS6gjrZQdlMf7a32JsSZzdrLc7MitWCAA6NTXeBs/edit?usp=sharing"


conn = st.connection("gsheets", type=GSheetsConnection)

data = conn.read(spreadsheet=url)
st.dataframe(data)
