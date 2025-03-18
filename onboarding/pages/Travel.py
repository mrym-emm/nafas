# import streamlit as st
# import pydeck as pdk

# st.set_page_config(
#     page_title="NAFAS", page_icon="🚗", layout="wide", initial_sidebar_state="auto"
# )


# st.header("Plan your travel")


# # Define Malaysia's central coordinates (Kuala Lumpur)
# malaysia_view = pdk.ViewState(
#     latitude=3.139,
#     longitude=101.6869,
#     zoom=10,
# )

# # Create an empty pydeck map
# map_layer = pdk.Deck(
#     map_style="mapbox://styles/mapbox/light-v9", initial_view_state=malaysia_view
# )

# st.pydeck_chart(map_layer)
