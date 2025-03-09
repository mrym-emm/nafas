import streamlit as st

st.set_page_config(
    page_title="NAFAS", page_icon="🍃", layout="wide", initial_sidebar_state="collapsed"
)


# Load CSS
def load_css():
    with open("assets/styles_landing.css", "r") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


# apply css
load_css()

# landing page
st.markdown(
    """
    <div class = "container">
            <h1>༄ N A F A S ༄</h1>
            <h4>because everyone deserves the chance to breathe</h4>
    </div>

    """,
    unsafe_allow_html=True,
)


# st.sidebar.header("Links")
# st.sidebar.slider("Bill depth (mm)", 13.0, 21.5, 17.2)

st.markdown(
    """
    <div class="top-links">
        <a href="https://example.com/page1" target="_blank">Page 1</a>
        <a href="https://example.com/page2" target="_blank">Page 2</a>
    </div>
""",
    unsafe_allow_html=True,
)
