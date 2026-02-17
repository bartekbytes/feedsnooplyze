import streamlit as st
from auth import landing
from dashboard import main as dashboard
from customization import customization

# Inject custom CSS
st.markdown(
    """
    <style>
    /* All buttons */
    button:hover {
        background-color: red !important;
        color: white !important;  /* optional: change text color */
    }
    </style>
    """,
    unsafe_allow_html=True
)

# -----------------------------------
# Page config
# -----------------------------------
st.set_page_config(
    page_title="feedsnooplyze",
    page_icon="📰",
    layout="wide"
)

# --------------------
# Session state
# --------------------
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

# user = user Email
if "user" not in st.session_state:
    st.session_state["user"] = None

if "needs_customization" not in st.session_state:
    st.session_state.needs_customization = False


# --------------------
# Routing
# --------------------
if not st.session_state["logged_in"]:
    landing.show()
elif st.session_state["needs_customization"]:
    customization.show()
else:
    dashboard.show()