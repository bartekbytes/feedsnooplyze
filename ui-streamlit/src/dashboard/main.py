import streamlit as st
from dashboard import components, feeds, overview

def show():
    # --------------------
    # Sidebar menu
    # --------------------
    menu = ["🏠 Overview", "Feeds", "Reports", "Settings"]
    choice = st.sidebar.selectbox("Menu", menu)

    st.sidebar.write(f"**Logged in as:** {st.session_state.user}")
    if st.sidebar.button("Logout"):
        st.session_state["logged_in"] = False
        st.session_state["user"] = None
        st.rerun()

    # --------------------
    # Page content
    # --------------------
    if choice == "🏠 Overview":
        overview.overview_page()
    if choice == "Reports":
        components.reports()
    elif choice == "Feeds":
        feeds.show_feeds(500)
    elif choice == "Settings":
        components.settings()

    st.markdown("# haha")


#def logout():
#    st.session_state["logged_in"] = False
#    st.session_state["user"] = None
#    #st.rerun()